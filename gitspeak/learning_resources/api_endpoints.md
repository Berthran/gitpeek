### 1. List repositories for the authenticated user

**API endpoint**
`GET` /user/repos

**Request format**
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos
```
The `Authorization` header is the required header. Others are optional.

**Some Useful Query parameters**
- visibility (`str`):
show `all`, `public`, or `private` repositories. Default `all`
- sort (`str`): sort the repositories by `created`, `updated`, `pushed`, or `full_name`. Default `full_name`
- direction (`str`): sort repositories in `asc` when using `full_name` or `desc`. Default `asc`
- per_page (`interger`): display n number of repositories per page. Max `100`. Default `30`
- page(`integer`): display repositories on page n. Default `1`

**Statys Code**
| Code | Description |
| :-----:| :-----------: |
| 200 | OK |
| 401 | Requires authentication|
| 403 | Forbidden |
| 422 | Validation failed, or the endpoint has been spammed |


**Example Response**
```[
  {
    "id": 1296269,
    "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "owner": {
      "login": "octocat",
      "id": 1,
      "node_id": "MDQ6VXNlcjE=",
   ```

  
  ### 2. List repositories for a user
  **API endpoint**
  `GET` /users/USERNAME/repos
  
  **Request format**
```bash

curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/repos
```
The `Authorization` header is the required header. Others are optional.

**Some Useful Query parameters**
- username(`str` + `required`): the handle for the GitHub user account
- type(`str`): show repositories of the the types `all`, `owner` or `member`. Default `owner`
- sort (`str`): sort the repositories by `created`, `updated`, `pushed`, or `full_name`. Default `full_name`
- direction (`str`): sort repositories in `asc` when using `full_name` or `desc`. Default `asc`
- per_page (`interger`): display n number of repositories per page. Max `100`. Default `30`
- page(`integer`): display repositories on page n. Default `1`


### 3. Get rate limit status for the authenticated user
**API endpoint**
  `GET` /rate_limit
  
  **Request format**
  ```bash
  curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/rate_limit
  ```