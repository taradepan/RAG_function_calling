tools = [
        {
            "type": "function",
            "function": {
                "name": "search_db",
                "description": "Get the data related to people using vector search. Provide the text to perform vector search in the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "text to perform vector search in the database",
                        },
                    },
                    "required": ["input"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "upload_db",
                "description": "Upload data to the database, don't forget to provide the name, age, and city of the person, only call this function when you have all 3 parameters. If anything is missing ask the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the person"},
                        "age": {"type": "integer", "description": "Age of the person"},
                        "city": {"type": "string", "description": "City where the person lives"},
                    },
                    "required": ["name", "age", "city"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_db",
                "description": "Delete data from the database, provide the ID of the person to delete the data from the database. to perform this first run the search_db function to get the ID of the person.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string", "description": "ID of the person"},
                    },
                    "required": ["id"],
                },
            },
        }
    ]