pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        },
    }
}

# This schema was completed by applicant Andrea Altenkirch, GitHub user: Testadora on 2/9/26, as part of the optional task #3 in the TODO list
order = {
    "type": "object",
    "required": ["pet_id"],
    "properties": {
        "id": {
            "type": "string"
        },
        "pet_id": {
            "type": "integer"
        }
    }
}