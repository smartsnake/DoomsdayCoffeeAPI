
# Getting Started

1. Install Docker
    * [Windows](https://download.docker.com/win/stable/Docker%20Desktop%20Installer.exe) and [Mac](https://download.docker.com/mac/stable/Docker.dmg)

2. Run docker

## Starting API

To run the API locally, run the following command in the project directory.

`docker-compose up --build`

This will download and build all required files for the api.

You can check by going to:

http://localhost:8080/home

Going to this address should return a JSON file.

## Stopping API

To stop the API run the following command.

`docker-compose down --rmi all`

This will stop all containers and remove them.

# API Paths

Below is all the availible Paths and supported methods

## /Home Method: (get)

Going to http://localhost:8080/home will return a JSON array with each object containing the following attributes.

```
{
    "id":"hash",
    "taken_at_timestamp":"timestamp", 
    "display_url":"url to image", 
    "caption":"text for that image"
}
```

This collection will be autopopulated based on doomsday's instagram.

## /foods Method: (get)

Going to http://localhost:8080/foods will return a JSON array with each object containing the following attributes.

```
{
    "id":"hash",
    "Name":"name of food", 
    "Price":"price for food", 
    "image":"image stored as base64",
    "ingredients":[
        "array", "of", "ingredients"
    ]
}
```

## /drinks Method: (get)

Going to http://localhost:8080/drinks will return a JSON array with each object containing the following attributes.

```
{
    "id":"hash",
    "Name":"name of drink", 
    "Price":"price for drink", 
    "image":"image stored as base64",
    "ingredients":[
        "array", "of", "ingredients"
    ]
}
```

## /food Method: (post)

Sending a POST request to localhost:8080/food with a JSON object will be saved to the food collections. Expected JSON structure.

```
{
    "Name":"name of food", 
    "Price":"price for food", 
    "image":"image stored as base64",
    "ingredients":[
        "array", "of", "ingredients"
    ]
}
```

## /drink Method: (post)

Sending a POST request to localhost:8080/drink with a JSON object will be saved to the food collections. Expected JSON structure.

```
{
    "Name":"name of drink", 
    "Price":"price for drink", 
    "image":"image stored as base64",
    "ingredients":[
        "array", "of", "ingredients"
    ]
}