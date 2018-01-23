from urllib.parse import quote
from uuid import uuid4
import requests

from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler

    
# Function to get list of url's from the dictionary list of predictions
def getUrl(dataList):
    resultList = []
    template_string = "https://www.google.com/maps/search/?api=1&query=" 
    for data in dataList:
        resultList.append(template_string + "%" + "&query_place_id=" + data['place_id'] )
    return resultList

#Function to get list of descriptions from the dictionary list of predictions 
def getDescription(dataList):
    descriptionList = []
    for data in dataList:
        descriptionList.append(data['description'])
    return descriptionList

def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    search_url_template = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="
    query = quote(query)
    api_key = "<YOUR API KEY>"
    search_url = search_url_template+query+"&key="+api_key
    data= requests.get(search_url).json()
    queryResults = []

    # Loop to get dictionary list of predictions(Description, Place ID)
    for record in data['predictions']:
        result = {}
        result['description'] = record['description']
        result['place_id'] = record['place_id']
        queryResults.append(result)
    
    dataList = getUrl(queryResults)
    titleList = getDescription(queryResults)
    results = []
    for idx, title in enumerate(titleList):
        results.append(
                InlineQueryResultArticle(
                    id = uuid4(),
                    title = titleList[idx],
                    input_message_content = InputTextMessageContent(dataList[idx])
                    )
            )
    update.inline_query.answer(results)


def main():
    # Create the Updater and pass it your bot's token.
    
    
    updater = Updater("<YOUR TOKEN>")#@findmapbot

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
