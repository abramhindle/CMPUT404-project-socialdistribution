Onboarding
===================================

Hello! This is an onboarding document that demonstrates how to locally test your app against our app (team 14). Local integration between the apps should simulate how our deployed apps on Heroku would integrate. Shout out to Team 10 for coming up with idea of creating such onboarding documents!

## Local Setup
1. At first, run the [database setup instructions (optional)](https://github.com/zarifmahfuz/project-socialdistribution#database) and the [backend setup instructions](https://github.com/zarifmahfuz/project-socialdistribution#backend). Do not seed any data into the database yet (see next steps).
2. Then, run the [frontend setup instructions](https://github.com/zarifmahfuz/project-socialdistribution/tree/master/frontend#running-the-front-end).
3. `cd backend && python manage.py loaddata local_seed`
4. Now, add your (local) node into our local node by making a local API request [as shown here](https://github.com/zarifmahfuz/project-socialdistribution#add-a-node-to-connect-with).
  * Use `username:admin` and `password:local-admin-password` for authorization
  * The request url is going to be something like `http://127.0.0.1:8000/api/nodes/` if you are running our server on port `8000`.
  * Specify `api_url` as the URL at which we are going to send requests to.
  * Note the `node_name` and `password` fields. This is what your node will need to connect to our node via HTTP Basic Auth.
5. Test that you can connect to our local node by sending a GET request to `http://127.0.0.1:8000/api/authors/` (assumes port 8000) with `username:<node_name>` and `password:<password>`. Similarly, test that our node can connect to your node by sending a similar API request to your node with `username:<auth_username>` and `password:<auth_password`.
6. Enjoy 🎉
