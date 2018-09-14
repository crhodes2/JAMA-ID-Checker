# !/usr/bin/env python3
# -*- mode: python -*-
##############################
''' JAMA ID CHECKER '''
##############################

''' A GitHub Integrated Service developed with Flask and Python aimed at automating bidirectional traceability '''
''' The goal is to verify that changes in GitHub repositories are easily traceable to Jama Connect repositories '''


#  MODULES #############################################################################################################

from flask import Flask, request
import os, time, re, runProg, logging, buildURL
from ghas import GitHubAppSession, JamaOauthSession

app = Flask(__name__)
APP_ID = os.getenv('APP_ID')
PK = os.getenv('PK')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


#    VARIABLES    ######################################################################################################


# Jama Pattern Reg Exr - The Regular Expression used at Jama Software----------------------

jama_pattern = re.compile(r'([A-Z]{1,10}-[A-Z]{1,5}-[0-9]{1,5})((?=\W)|$)')
JAMA_URL = 'https://www.jamaland.com'
logger = runProg.logger

#    FUNCTIONS    ######################################################################################################


#   PENDING STATUS BADGE PAYROLL METHOD----------------------------------------------------


''' A payroll method sent to GitHub to change badge status to Pending '''


def buildPending(pending_msg_text=None):
    payloadPending = {"state": "pending", "target_url": "http://www.jamaland.com", "description": pending_msg_text, "context": "JAMA ID Check: "}
    return payloadPending

#   SUCCESS STATUS BADGE PAYROLL METHOD----------------------------------------------------


''' Payload method sent to GitHub, displaying a success badge '''


def buildSuccess(success_msg_text=None):
    payloadPending = {"state": "success", "target_url": "http://www.jamaland.com", "description": success_msg_text, "context": "JAMA ID Check: "}
    return payloadPending

#   FAILURE STATUS BADGE PAYROLL METHOD----------------------------------------------------


''' Payload method sent to GitHub, displaying a failure badge '''


def buildFailure(failing_msg_text=None):
    payloadPending = {"state": "failure", "target_url": "http://www.jamaland.com", "description": failing_msg_text, "context": "JAMA ID Check: "}
    return payloadPending

#   COUNT NUMBER OF COMMITS METHOD---------------------------------------------------------


''' Method to calculate the Number of Commits Available in a Pull Request '''


def calculating_Number_Of_Commits(jsonRequest, completeStatusUrl):
    jsonRequest = request.json  # jSON Get Request Variable: Get Request that Flask received from GitHub
    completeStatusUrl = jsonRequest["pull_request"]["statuses_url"]  # jSON object: Status URL from every Pull Request
    print("Receiving Pull Request from GitHub... ...please wait")
    time.sleep(10)



#    MAIN FUNCTION    ##################################################################################################


#   A GET and POST Request method that handles communication between GitHub and the Flask Application


''' 
It handles a GET and POST request. If the Request is a GET, it does nothing. If it is a POST, it handles the communication. 
In a POST request, As soon as a Pull Request is created on GitHub, Flask server sends POST Request to GitHub for status to get changed from neutral to pending.
It then does a commit count and gives a success or a failure badge, depending on the Pull Request status.
'''


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return "Welcome to Flask App. Documentation on How to Use the GitHub Application goes here"


#   SEND IN STATUS TO POST REQUEST TO GITHUB AS A PENDING BADGE AND START CHECK THROUGH THE PULL REQUEST

    jsonRequest = request.json  # jSON Get Request Variable: Get Request that Flask received from GitHub
    eventAction = jsonRequest["action"]  # jSON object: Total access to events of a Pull Request

    if eventAction != 'closed':
        jama_session = JamaOauthSession(JAMA_URL, CLIENT_ID, CLIENT_SECRET)
        installation_id = jsonRequest['installation']['id']
        with GitHubAppSession(APP_ID, PK, installation_id) as requests:
            completeStatusUrl = jsonRequest["pull_request"][
                "statuses_url"]  # jSON object: The Status URL from every Pull Request
            commitUrl = jsonRequest["pull_request"][
                "commits_url"]  # jSON object: The URL of every info in a Pull Request, including commit messages
            listofCommits = requests.get(url=commitUrl).json()  # jSON object: Access to PR info + commit messages

            print("--------------------------------------------------------------------------")
            print("--------------------------------------------------------------------------")

            runProg.start()

            #   FLASK SERVER DOES A REGEXPR CHECK, LISTING OUT ALL THE COMMIT MESSAGES FOUND IN PR

            commitNumber = jsonRequest["pull_request"]["commits"]  # Integer: Number of commits in every Pull Request

            logger.info('\n')
            logger.info('\n')
            logger.info("------------------------- JAMA ID CHECKER --------------------------")
            logger.info("----------------------------- RESULTS ------------------------------")
            logger.info('\n')

            logger.info("eventAction = " + str(eventAction))
            print("eventAction = " + str(eventAction))

            print("\n")
            logger.info("" + str(commitNumber) + " Commit Message(s) Found ------------------")
            logger.info("\n")

            for c in listofCommits:
                logger.info('-> ' + c["commit"]["message"])
                time.sleep(0.2)

            failedlogger = logging.getLogger(__name__)
            for co in listofCommits:
                if not (jama_pattern.search(co["commit"]["message"])):
                    failedlogger.error('-> ' + co["commit"]["message"])

            #   FLASK SERVER GIVES ITS VERDICT: FAILURE OR SUCCESS, ON THE REGEXPR CHECK

            failed_msg_text = []
            for com in listofCommits:
                search_results = jama_pattern.search(com["commit"]["message"])
                if not search_results:
                    failed_msg_text.append(com["commit"]["message"])
                    time.sleep(0.2)
                else:
                    print("\n")
                    logger.info("Document Key(s) Found --------------------------------------------")
                    documentKey = search_results.group(0)
                    logger.info(buildURL.templateURL(documentKey))
                    response = jama_session.get(buildURL.templateURL(documentKey))
                    resultCount = response.json()['meta']['pageInfo']['resultCount']

                    if resultCount != 1:
                        logger.error("{} Jama IDs not found in Jamaland".format(documentKey))
                        failed_msg_text.append(co["commit"]["message"])

                    time.sleep(0.2)

            print("\n")

            if (len(failed_msg_text) != 0):
                logger.info("---------------------------- REGEXR CHECK RESULT - Failure -----------------------\n")
                failed_msg_string = 'Invalid JAMA IDs Found: ' + ', '.join(failed_msg_text)[:123]
                print(failed_msg_string)
                evenResponse = requests.post(url=completeStatusUrl, json=buildFailure(failed_msg_string))
                # print(evenResponse.text, evenResponse.json())
            else:
                logger.info("------------------------ REGEXR CHECK RESULT - Success ---------------------------\n")
                evenResponse = requests.post(url=completeStatusUrl, json=buildSuccess(success_msg_text='OK'))

    else:
        runProg.closed()

    return "\n"



#    MAIN    ###########################################################################################################

if __name__ == "__main__":

    app.run(debug=False)

########################################################################################################################
