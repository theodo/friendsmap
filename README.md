Theodo Friends Map
==================

Sandbox application to display Facebook contacts over a Google map, using MongoDB as a cache backend.

Installation
------------

1. You need to create a Facebook application in order to use their web services. Please refer to [their documentation][1].
2. On the *Basic* tab of your application's settings, enter '**http://localhost:8080**' in the *Website with Facebook Login* section.
3. We use [FOSFacebookBundle][2] as a wrapper for the Facebook API. Retrieve your **App ID** and **App Secret** and add them to `app/config/config.yml`.
4. If you don't already have it installed locally, [download composer][3].
5. `php composer.phar install`
6. Set up your favourite web server to serve the `web` directory on `localhost:8080`. If you're blessed with PHP >= 5.4, congratulations `app/console server:run localhost:8080` and you're done. If not, the easiest would be to set up [symfttpd][4].

You're done! Open `http://localhost:8080/app_dev.php`

[1]: https://developers.facebook.com/docs/appsonfacebook/tutorial/
[2]: https://github.com/FriendsOfSymfony/FOSFacebookBundle
[3]: http://getcomposer.org/doc/00-intro.md#installation
[4]: https://github.com/laurentb/symfttpd
