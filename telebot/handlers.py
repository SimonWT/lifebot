def init_bot(bot, update_queue):
    # Create bot, update queue and dispatcher instances
    dispatcher = Dispatcher(bot, update_queue)

    ##### Register handlers here #####
    
    start_handler = CommandHandler('start', tghandlers.startCommand)
    dispatcher.add_handler(start_handler)
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    
    return update_queue

def startCommand(update, context):
    context.message.reply_text('Hi!')