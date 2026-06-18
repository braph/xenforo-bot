### {url}/psychose/index.php?chat/update

POST data:

```json
{
    "users":                {"1": [1441, 2498, 2180, 2299]},
    "channel":              "room",
    "room_id":              "1",
    "last_id":              {"1": last_id},
    "conv_id":              0,
    "conv_unread":          [],
    "conv_only":            0,
    "conv_items":           "",
    "conv_last_active":     t,
    "conv_last_update":     t,
    "user_last_update":     t,
    "is_chat_page":         1,
    "hide_tabs":            0,
    "_xfResponseType":      "json",
    "_xfWithData":          1,
    "_xfRequestUri":        "/psychose/chat/",
    "_xfToken":             self.xf_token
}
```

### {rl}/psychose/index.php?chat/submit

POST data:

```json
{
    "users":            { "1": [ 2498, 2180, "1968", "2762", "2299", "1441" ] },
    "channel":          "room",
    "room_id":          "1",
    "last_id":          { "1": 94762 },
    "conv_id":          0,
    "conv_items":       "",
    "conv_unread":      [],
    "conv_last_id":     0,
    "message_html":     message_html,
    "_xfResponseType": "json",
    "_xfWithData":      1,
    "_xfRequestUri":    "/psychose/chat/",
    "_xfToken":         self.xf_token
}
