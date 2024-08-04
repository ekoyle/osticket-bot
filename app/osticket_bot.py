import json
import mysql.connector
from mysql.connector import Error
import requests
import sys
import getopt
import datetime;
import configparser
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def report(config, channel, message):
    print("Channel: %s " % channel)
    print("Message: %s " % message)
    client = WebClient(config['slack']['oauth_token'])
    try:
        response = client.chat_postMessage(channel=channel, text=message)
        print(response)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

def pullTickets(config):
    tickets = None

    # FIXME: make sure our table exists?
    # create table slack_ticket ( ticket_id int unsigned not null, slack_last_notified datetime not null, PRIMARY KEY (ticket_id));

    try:
        connection = mysql.connector.connect(host=config['mysql']['host'],
                                         database=config['mysql']['database'],
                                         user=config['mysql']['user'],
                                         password=config['mysql']['password'])
    
        sql_select_Query = """
        SELECT
            ost_ticket.ticket_id,
            subject,
            CASE
                WHEN closed IS NOT NULL
                    THEN 'Closed Ticket'
                WHEN lastreported IS NULL
                    THEN 'New Ticket'
                WHEN lastupdate < DATE_ADD(NOW(), INTERVAL -60 MINUTE)
                    THEN 'Update Needed for Ticket'
                ELSE ''
            END AS slack_state
            FROM osticket_db.ost_ticket
                JOIN osticket_db.ost_ticket__cdata
                ON osticket_db.ost_ticket__cdata.ticket_id  = osticket_db.ost_ticket.ticket_id
                LEFT OUTER JOIN osticket_db.slack_ticket
                ON osticket_db.ost_ticket.ticket_id = osticket_db.slack_ticket.ticket_id
            WHERE
                (
                    slack_last_notified IS NULL
                      OR GREATEST(slack_last_notified, lastupdate) < DATE_ADD(NOW(), INTERVAL -60 MINUTE)
                      OR closed IS NOT NULL AND slack_last_notified < closed
                )

        """
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        tickets =  records 
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    return tickets

def updateTicket(config,id):

    try:
        connection = mysql.connector.connect(host=config['mysql']['host'],
                                         database=config['mysql']['database'],
                                         user=config['mysql']['user'],
                                         password=config['mysql']['password'])
        cursor = connection.cursor(dictionary=True)
        print("Id: %s"% id)
        update_query = """
        INSERT INTO slack_ticket (ticket_id, slack_last_notified)
          VALUES (%s, now())
          ON DUPLICATE KEY UPDATE"""
        input_data = (id,)
        cursor.execute(update_query,input_data)
        connection.commit()
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

  
def main():
    running = True 

    config = configparser.ConfigParser()
    config.read('botconfig.ini')
    print(config.sections())
    verbose = 0 
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "v")
    except:
        print("Error")

    for opt, arg in opts:

        if opt in ['-v']:
            verbose = 1
    while running: 
        tickets = pullTickets(config)
        time.sleep(1)
        print(tickets)
        for ticket in tickets:
            print(config['slack']['channel'])
            url = config['default']['url'] 
            message = (
                f"{ticket['slack_state']!s:<12}: {ticket['subject']}, "
                f"url: https://{url}/upload/scp/tickets.php?id={ticket['ticket_id']}"
            )
            report(config,config['slack']['channel'],message)
            updateTicket(config, ticket["ticket_id"])



if __name__ == "__main__":
    main()
