# Just Give Me The Damn Recipe (Website with Authentication)

![alt text](https://github.com/K2-XT/JGMTDRWebsite/blob/main/jgmtdr_screenshot.png?raw=true)

## Overview

IF DEMOING ON CHROME, SAMESITE PROTECTIONS MUST BE DISABLED: https://support.siteimprove.com/hc/en-gb/articles/360007364778-Turning-off-Google-Chrome-SameSite-Cookie-Enforcement

This is a companion website to the Just Give Me The Damn Recipe app I made for my iOS Development class at Dixie State University. The database was created with SQLite3; the server with python3; the front-end with HTML, CSS, and Javascript. I considered making this a private project for just my extended family. However, I hadn't had any experience in Android yet, and wanted to wait until then. I eventually decided that my family would most likely not use the app, and didn't want to pay hosting costs.

This project shows effective web development skills in designing clean, pretty, and functional UI (in my opinion). All authentication is encrpyted on the back-end, and the database is clean and organized. This project also demonstrates basic python skills.


## Resource

**Recipe**

Attributes:

* title (string)
* date (string, generated automatically)
* diet (string)
* ingredients (string)
* instructions (string)

Inserting:

```sql
INSERT INTO recipes 
(title, date, diet, ingredients, instructions) 
VALUES 
('RecipeTitle', date('now'), 'RecipeDiet', 'RecipeIngredients', 'RecipeInstructions');
```

**User**

Attributes:

* firstName (string)
* lastName (string)
* email (string)
* password (string) Password is hashed with bcrypt on the server before it is inserted into the database.

Inserting:

```sql
INSERT INTO users 
(firstName, lastName, email, password) 
VALUES 
('test', 'user', 'testuser@dmail.dixie.edu', 'testpassword');
```

## Schema

```sql
CREATE TABLE recipes (
id INTEGER PRIMARY KEY,
title TEXT,
date TEXT,
diet TEXT,
ingredients TEXT,
instructions TEXT);
```

```sql
CREATE TABLE users (
id INTEGER PRIMARY KEY,
firstName TEXT,
lastName TEXT,
email TEXT,
password TEXT);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Retrieve recipes collection    | GET    | /recipes
Retrieve recipe member         | GET    | /recipes/*\<id\>*
Create recipe member           | POST   | /recipes
Update recipe member           | PUT    | /recipes/*\<id\>*
Delete recipe member           | DELETE | /recipes/*\<id\>*
Create user member	       | POST   | /users
Create session 		       | POST   | /sessions
Delete session		       | DELETE | /sessions
