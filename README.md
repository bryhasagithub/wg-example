# wg-example
The application is a small REST API to display file information from a portion of the user’s file system. The user will specify a root directory when launching the application. All directories from the root on downward are then browsable using the REST API.

## Example REST APIs
```
GET / -> list contents of foo/ (e.g. foo1, foo2, bar/)
GET /bar -> list contents of foo/bar/ (e.g bar1, baz/)
GET /foo1 -> contents of file foo/foo1
GET /bar/bar1 -> contents of file foo/bar
```

### Specification Details
  - REST API should return responses in JSON in an appropriate fashio utilizing best practices.
  - Reports all files in directory responses, including hidden files. You should report file name, owner, size, and permissions (read/write/execute - standard octal representation is acceptable).
  - Assume that all files are text files of modest size (i.e., that can fit comfortably within a JSON blob)
  - API documentation included
  - Application is Dockerized.
  - Provide a shell script to actually run the app from the command line.
  - Has multiple unit tests that presents themselves as examples of testing strategy.

#### TODO if phase 1 is complete
  - Create POST, PUT, and DELETE endpoints to add, replace, and delete directories and files as appropriate. Any request bodies should be JSON.
  - Document your API using Swagger.
  - Create a Helm chart.

### Running Locally  
```sh
$ git clone https://github.com/bryhasagithub/wg-example
$ pip install Flask
$ python main
```
