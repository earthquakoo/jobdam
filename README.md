
<h1 align="center">🙏 Jobdam - Terminal TUI open chatting APP  🙏</h1>

<h4 align="center">Enjoy simple open chatting in the terminal!</h4>

<p align="center"><img src="/resources/jobdam-gif.gif"></img></center>

# Introduction

`Jobdam`, meaning "chat, small talk, chitchat" in Korean, is a TUI (Text User Interface) open chatting application built with a simple UI. It allows anyone to easily engage in open chatting in the terminal without the need for authentication or sign-up.


# 🛎 Current Version `0.1.6`

#### Upgrade with `pip install jobdam --upgrade`

# 🚀 Installation & Settings

- Requires Python version `>3.11` to be installed.
- Installable in the terminal using the following command:

```bash
pip install jobdam
```

Some shells can damage the UI, and we recommend it to be used on the full screen, preferably.

# 👨‍💻 Instructions

- The screen consists of various widgets. You can navigate conveniently with the TAB key and select a Room using the up and down arrow keys.
- To create a Room, you need to input Room Name, Tag, and Maximum people. The Maximum people limit is up to 10.
- Owners can ban guests and change room settings.
- You can create three rooms per account.

# 📸 Screenshot
## Main

Navigate up and down using the `TAB` key and select with the `Enter` key.

![](image/main.png)

## Register

Similar to the main screen, navigate with the `TAB` key. The green text in the center corresponds to the `validator` for each input field.

![](image/register.png)
## Login

Similar to the register screen.

![](image/login.png)
## Search Screen

- The left side shows the rooms you've joined, and the center lists rooms created by other users.
- The input field at the top center allows you to search for rooms by Room name or `#tag`.
	- e.g., `#Language`

![](image/search-room.png)
## Create room Screen

Clicking the Create Room button on the search screen brings up the following screen.
- Set `Room Name`, `Tag`, and `Maximum people`, each with its own `validator`.

![](image/create-room.png)

## Chat room Screen

- The left side displays rooms you've joined. If it's your room, you can join another room at any time.
- The main center screen shows the chat history.
- The right screen lists the people in the room. Owners can ban unwanted guests with the `Enter` key.
- The `Setting` button at the bottom left allows owners to change room settings.
- The `Exit` button deletes the room if you're the owner or simply exits the joined room if you're a guest.

![](image/chat-room.png)

# 💬 Remarks

When entering a room, a WebSocket connection is established, and the connection is immediately terminated upon exiting the app.

I wanted the WebSocket to persist for the duration of the access token's validity to send notifications. However, I have not yet found a way to maintain it with my limited knowledge.

I will strive to make this possible as quickly as possible.


# 🚮 Uninstalling

If, by any chance, due to unforeseen circumstances, you wish to uninstall, you can do so with the following command:

```bash
pip uninstall jobdam
```