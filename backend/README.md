# Backend

There is a little bit of documentation for backend part of this project.
Here I'll leave my notes and explanations why I did something this or that way.

## Database
### Overall Structure
The main entity is a `Form`, it has `Questions`.
`Submission` is created when someone is filling the `Form`. It is related to a certain `Form` and has `Answers`, which are related to certain `Questions`

### Form
`Form`'s id field is a bit tricky. Basically, it's an UUID, but encoded in Base62. That was made for better readability, e.g. in URL

### Question
#### Fields
**Short explanation:**

There are two groups of fields. First one contains main fields and the second one - fields for validation purposes

**Validation fields**

*Explanation of fields, that aren't obvious*

`max_value` and `min_value` - have to be integers if `is_float` is `False` or `None` and floats otherwise

`choices` - JSON list with objects like {"answer": "...", "meta": {...}} where meta is some display data (like `type`, `filename`, etc.)


## Auth
### JWT
The authentication works via JWT. Tokens are sent in a form of http-only cookie, so that frontend won't worry about securely storing them (and yes, I know about sessions existence).
Maybe I'll add an endpoint to get the tokens in a usual form, but at the moment I don't need it. 
