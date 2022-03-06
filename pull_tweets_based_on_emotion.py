
queries_base = {
"happy": [
            '😁',
            '😀',
            '🤗',
            '😆',
            '😃',
            '🙂'
        ],
"sad":[
            '😭',
            '😭',
            '😔',
            '😥',
            '😞',
            '☹️']
}

def assemble_queries(queries_base):
    """Makes more compelx queries string from a dirctionary indexed by emtions 
    each containing a list of chraters revevant to the emotion."""
    
    #Makes another dict which contains two items indexed by emotions and containg a string of associted emojis
    query_base_as_string = {}
    for emotions, emoji_list in queries_base.items():
        emoji_string = ""
        
        for emoji in emoji_list:
            emoji_string += emoji

        query_base_as_string[emotions] = emoji_string
        
    #Goes through each emote and makes a more compelx query string
    final_query_list = []
    
    for emotions, emoji_list in queries_base.items():
        query = f"🚀"
        for emoji in emoji_list:
            emoji_string += emoji

        query_base_as_string[emotions] = emoji_string