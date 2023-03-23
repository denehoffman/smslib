# smslib
### A *very simple* library for sending *very simple* text messages via SMS-to-email gateways

I often run code on a remote computer cluster, and sometimes this code takes a very long time to run. This project was inspired by a desire to receive a notification on my phone when my programs wrap up, *without* using a fancy API, installing a third-party messaging program, and (most importantly) paying money. After all, I already pay to send and recieve texts, and email is free these days. Most common US phone providers have a way to send texts via an email. For example, if your phone number is `+1-(123)-456-7890`, and your service provider is AT&T, you can, right now, send yourself a text message by emailing `1234567890@txt.att.net`. This is the core idea behind the library.

## Installation
This package is available via PyPI:
```sh
$ pip install smslib
```
Alternatively, clone the repo and install it manually:
```sh
$ git clone git@github.com:denehoffman/smslib.git
$ cd smslib
$ pip install .
```

## Usage
### In a python script
There are several ways to use the package. It contains three submodules, `sender`, `receiver`, and `notify`. To manually use the library inside python, ignore the `notify` submodule and write something like the following:
```python
import smslib
sender = smslib.Sender("my_email@gmail.com", "mypassword", "smtp.gmail.com")
receiver = smslib.Receiver("123-456-7890", "at&t")
sender.send_message("Hello world!", receiver)
```
That's pretty much all of the core functionality. Note that for GMail, if you have 2FA turned on, you might need to create an [app password](https://support.google.com/accounts/answer/185833?hl=en). If everything works correctly, you should get a text message that says `"Hello world"`! The package uses `smtplib`'s [`SMTP.send_message`](https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.send_message) function (under [TLS encryption](https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.starttls)), so feel free to use an [`email.message.Message`](https://docs.python.org/3/library/email.compat32-message.html#email.message.Message) object instead of a `string`. There is also the option to send a regular email instead of a text (or maybe it's a text to a phone provider that isn't in the default list) by specifying an email address in to the `Receiver`:
```python
receiver = smslib.Receiver(None, None, email="my.friends.email@university.edu")
```
You can also specify an [ssl.SSLContext](https://docs.python.org/3/library/ssl.html#ssl.SSLContext) using a `context` keyword argument in `send_message`. Additionally, a port can be specified using the `port` keyword argument in `smslib.Sender`, although the default, 587, should be sufficient for most use cases.

### In a shell script
The other way to use the library is through a simple command-line interface. This gets built automatically when installed, and the command is called `notify`. I realize this has the potential to conflict with some other programs, which is why I would advise the use of a virtual python environment.
```sh
$ notify --help
usage: notify [-h] [--sender SENDER] [--receiver RECEIVER] [--email EMAIL] [--password PASSWORD]
              [--smtp-server SMTP_SERVER] [--port PORT] [--phone-number PHONE_NUMBER]
              [--provider PROVIDER] [--confirm]
              message

Send an SMS via email Available SMS providers: verizon, at&t, att, tmobile, sprint, boost

positional arguments:
  message               Message string to send

optional arguments:
  -h, --help            show this help message and exit
  --sender SENDER       Sender name from ~/.smslibrc.toml
  --receiver RECEIVER   Receiver name from ~/.smslibrc.toml
  --email EMAIL         Sender's email address
  --password PASSWORD   Sender's password
  --smtp-server SMTP_SERVER
                        Sender's SMTP server
  --port PORT           Sender's SMTP server port
  --phone-number PHONE_NUMBER
                        Receiver's phone number
  --provider PROVIDER   Receiver's phone provider
  --confirm             Print confirmation after sending message
```
This contains all of the fields above (note that `--port` is completely optional and has a default value of 587) with two additional arguments, `--sender` and `--receiver`. I set this up to cut down on the hastle of entering in all the information in a long shell command every time. By default, it will look for a TOML file located in your home directory. An example is as follows:
```toml
# ~/.smslibrc.toml

[senders]
[senders.myself]
email = "my.email@gmail.com"
password = "mypassword"
smtp_server = "smtp.gmail.com"
port = 587

[receivers]
[receivers.myfriend]
phone_number = "123-456-7890"
provider = "att"
```
Then we can just call the `notify` command as
```sh
$ notify "Hello world!" --sender myself --receiver myfriend
```
This file can be located anywhere, and the default location can be overwritten by setting the `$SMSLIBRC` environment variable to point to the desired path. Any command-line arguments here will have precedence over the `.smslibrc.toml` file. For example
```sh
$ notify "Hello world!" --sender myself --receiver myfriend --port 123
```
will send the message over port 123 rather than the 587 specified in the file. Furthermore, while there was an option to send a message to any custom email address via the `email` keyword in `smslib.Receiver`, there is no command-line option for this. However, adding an `email` field to the corresponding reciever in `.smslibrc.toml` will give you this functionality in the shell.

Finally, any fields which are not specified explicitly will be acquired by prompting the user in shell. All of these are raw input fields, with the exception of the sender's password, which uses [`getpass`](https://docs.python.org/3/library/getpass.html) to hide the password input. It is usually not the best practice to store your passwords in code or in a configuration file, but I allow this as an option because GMail's "app passwords" are randomly generated strings which are not easy to type or remember.

## Changelog
- v1.0.0
    - Initial commit with base functionality

## Planned Features
None so far, but I'm sure I'll think of a few things. If anyone reading this has suggestions, let me know!
