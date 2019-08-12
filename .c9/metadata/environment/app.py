{"changed":true,"filter":false,"title":"app.py","tooltip":"/app.py","value":"import os\nfrom flask import Flask, render_template, redirect, request, url_for, session, flash\nfrom flask_pymongo import PyMongo\nfrom bson.objectid import ObjectId\n\napp = Flask(__name__)\napp.secret_key = os.getenv(\"SECRET_KEY\")\napp.config[\"MONGO_DBNAME\"]=\"CookBook\"\napp.config[\"MONGO_URI\"]=os.getenv(\"MONGO_URI\")\n\nmongo=PyMongo(app)\n\n@app.route(\"/\")\ndef index():\n    return render_template(\"index.html\")\n   \n   \n@app.route(\"/login\")\ndef login():\n    return render_template(\"login.html\")\n    \n# New user registration template.\n@app.route('/new_user')\ndef new_user():\n    return render_template('new_user.html')  \n\n# New user registration submit\n@app.route('/new_user/register', methods=['GET','POST'])\ndef register():\n    user={}\n    users=mongo.db.users\n    username=request.form['user']\n    # It checks if the user name is not being used before\n    if users.find_one({\"user\":username}):\n        flash('Username not valid, already taken.')\n        return redirect(url_for('new_user'))\n    else: \n        # User name valid as new user, redirecting to the login page\n        user[\"user\"]=username\n        user[\"password\"]=request.form['password']\n        users.insert_one(user)\n        flash('User created. You can now login.')\n        return redirect(url_for('autentication'))\n            \n@app.route(\"/recipes\")\ndef recipes():\n    return render_template(\"recipes.html\")\n    \n@app.route(\"/favourites\")\ndef favourites():\n    return render_template(\"favourites.html\")\n    \n    \n    \nif __name__ == \"__main__\":\n    app.run(host=os.environ.get(\"IP\"),\n            port=int(os.environ.get(\"PORT\")),\n            debug=True)","undoManager":{"mark":94,"position":100,"stack":[[{"start":{"row":10,"column":13},"end":{"row":10,"column":14},"action":"insert","lines":[":"],"id":109}],[{"start":{"row":10,"column":14},"end":{"row":11,"column":0},"action":"insert","lines":["",""],"id":110},{"start":{"row":11,"column":0},"end":{"row":11,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":11,"column":4},"end":{"row":11,"column":5},"action":"insert","lines":["r"],"id":111},{"start":{"row":11,"column":5},"end":{"row":11,"column":6},"action":"insert","lines":["e"]},{"start":{"row":11,"column":6},"end":{"row":11,"column":7},"action":"insert","lines":["t"]},{"start":{"row":11,"column":7},"end":{"row":11,"column":8},"action":"insert","lines":["u"]},{"start":{"row":11,"column":8},"end":{"row":11,"column":9},"action":"insert","lines":["r"]},{"start":{"row":11,"column":9},"end":{"row":11,"column":10},"action":"insert","lines":["n"]},{"start":{"row":11,"column":10},"end":{"row":11,"column":11},"action":"insert","lines":["_"]}],[{"start":{"row":11,"column":11},"end":{"row":11,"column":12},"action":"insert","lines":["r"],"id":112},{"start":{"row":11,"column":12},"end":{"row":11,"column":13},"action":"insert","lines":["e"]},{"start":{"row":11,"column":13},"end":{"row":11,"column":14},"action":"insert","lines":["n"]},{"start":{"row":11,"column":14},"end":{"row":11,"column":15},"action":"insert","lines":["d"]},{"start":{"row":11,"column":15},"end":{"row":11,"column":16},"action":"insert","lines":["e"]},{"start":{"row":11,"column":16},"end":{"row":11,"column":17},"action":"insert","lines":["r"]}],[{"start":{"row":11,"column":16},"end":{"row":11,"column":17},"action":"remove","lines":["r"],"id":113},{"start":{"row":11,"column":15},"end":{"row":11,"column":16},"action":"remove","lines":["e"]},{"start":{"row":11,"column":14},"end":{"row":11,"column":15},"action":"remove","lines":["d"]},{"start":{"row":11,"column":13},"end":{"row":11,"column":14},"action":"remove","lines":["n"]},{"start":{"row":11,"column":12},"end":{"row":11,"column":13},"action":"remove","lines":["e"]},{"start":{"row":11,"column":11},"end":{"row":11,"column":12},"action":"remove","lines":["r"]},{"start":{"row":11,"column":10},"end":{"row":11,"column":11},"action":"remove","lines":["_"]}],[{"start":{"row":11,"column":10},"end":{"row":11,"column":11},"action":"insert","lines":[" "],"id":114},{"start":{"row":11,"column":11},"end":{"row":11,"column":12},"action":"insert","lines":["r"]},{"start":{"row":11,"column":12},"end":{"row":11,"column":13},"action":"insert","lines":["e"]},{"start":{"row":11,"column":13},"end":{"row":11,"column":14},"action":"insert","lines":["n"]},{"start":{"row":11,"column":14},"end":{"row":11,"column":15},"action":"insert","lines":["d"]}],[{"start":{"row":11,"column":11},"end":{"row":11,"column":15},"action":"remove","lines":["rend"],"id":115},{"start":{"row":11,"column":11},"end":{"row":11,"column":26},"action":"insert","lines":["render_template"]}],[{"start":{"row":11,"column":26},"end":{"row":11,"column":28},"action":"insert","lines":["()"],"id":116}],[{"start":{"row":11,"column":27},"end":{"row":11,"column":29},"action":"insert","lines":["\"\""],"id":117}],[{"start":{"row":11,"column":28},"end":{"row":11,"column":29},"action":"insert","lines":["r"],"id":118},{"start":{"row":11,"column":29},"end":{"row":11,"column":30},"action":"insert","lines":["e"]},{"start":{"row":11,"column":30},"end":{"row":11,"column":31},"action":"insert","lines":["c"]},{"start":{"row":11,"column":31},"end":{"row":11,"column":32},"action":"insert","lines":["i"]},{"start":{"row":11,"column":32},"end":{"row":11,"column":33},"action":"insert","lines":["p"]},{"start":{"row":11,"column":33},"end":{"row":11,"column":34},"action":"insert","lines":["e"]},{"start":{"row":11,"column":34},"end":{"row":11,"column":35},"action":"insert","lines":["s"]},{"start":{"row":11,"column":35},"end":{"row":11,"column":36},"action":"insert","lines":["."]},{"start":{"row":11,"column":36},"end":{"row":11,"column":37},"action":"insert","lines":["h"]}],[{"start":{"row":11,"column":37},"end":{"row":11,"column":38},"action":"insert","lines":["t"],"id":119},{"start":{"row":11,"column":38},"end":{"row":11,"column":39},"action":"insert","lines":["m"]},{"start":{"row":11,"column":39},"end":{"row":11,"column":40},"action":"insert","lines":["l"]}],[{"start":{"row":12,"column":4},"end":{"row":13,"column":0},"action":"insert","lines":["",""],"id":120},{"start":{"row":13,"column":0},"end":{"row":13,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":13,"column":4},"end":{"row":14,"column":0},"action":"insert","lines":["",""],"id":121},{"start":{"row":14,"column":0},"end":{"row":14,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":7,"column":40},"end":{"row":8,"column":0},"action":"insert","lines":["",""],"id":122},{"start":{"row":8,"column":0},"end":{"row":8,"column":4},"action":"insert","lines":["    "]},{"start":{"row":8,"column":4},"end":{"row":9,"column":0},"action":"insert","lines":["",""]},{"start":{"row":9,"column":0},"end":{"row":9,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":9,"column":0},"end":{"row":9,"column":4},"action":"remove","lines":["    "],"id":123}],[{"start":{"row":9,"column":0},"end":{"row":9,"column":1},"action":"insert","lines":["@"],"id":124},{"start":{"row":9,"column":1},"end":{"row":9,"column":2},"action":"insert","lines":["a"]},{"start":{"row":9,"column":2},"end":{"row":9,"column":3},"action":"insert","lines":["p"]},{"start":{"row":9,"column":3},"end":{"row":9,"column":4},"action":"insert","lines":["p"]},{"start":{"row":9,"column":4},"end":{"row":9,"column":5},"action":"insert","lines":["."]}],[{"start":{"row":9,"column":5},"end":{"row":9,"column":6},"action":"insert","lines":["r"],"id":125},{"start":{"row":9,"column":6},"end":{"row":9,"column":7},"action":"insert","lines":["o"]},{"start":{"row":9,"column":7},"end":{"row":9,"column":8},"action":"insert","lines":["u"]},{"start":{"row":9,"column":8},"end":{"row":9,"column":9},"action":"insert","lines":["t"]},{"start":{"row":9,"column":9},"end":{"row":9,"column":10},"action":"insert","lines":["e"]}],[{"start":{"row":9,"column":10},"end":{"row":9,"column":12},"action":"insert","lines":["()"],"id":126}],[{"start":{"row":9,"column":11},"end":{"row":9,"column":13},"action":"insert","lines":["\"\""],"id":127}],[{"start":{"row":9,"column":12},"end":{"row":9,"column":13},"action":"insert","lines":["/"],"id":128},{"start":{"row":9,"column":13},"end":{"row":9,"column":14},"action":"insert","lines":["l"]},{"start":{"row":9,"column":14},"end":{"row":9,"column":15},"action":"insert","lines":["o"]},{"start":{"row":9,"column":15},"end":{"row":9,"column":16},"action":"insert","lines":["g"]},{"start":{"row":9,"column":16},"end":{"row":9,"column":17},"action":"insert","lines":["i"]}],[{"start":{"row":9,"column":17},"end":{"row":9,"column":18},"action":"insert","lines":["n"],"id":129}],[{"start":{"row":9,"column":20},"end":{"row":10,"column":0},"action":"insert","lines":["",""],"id":130},{"start":{"row":10,"column":0},"end":{"row":10,"column":1},"action":"insert","lines":["d"]},{"start":{"row":10,"column":1},"end":{"row":10,"column":2},"action":"insert","lines":["e"]}],[{"start":{"row":10,"column":2},"end":{"row":10,"column":3},"action":"insert","lines":["g"],"id":131}],[{"start":{"row":10,"column":2},"end":{"row":10,"column":3},"action":"remove","lines":["g"],"id":132}],[{"start":{"row":10,"column":2},"end":{"row":10,"column":3},"action":"insert","lines":["f"],"id":133}],[{"start":{"row":10,"column":3},"end":{"row":10,"column":4},"action":"insert","lines":[" "],"id":134},{"start":{"row":10,"column":4},"end":{"row":10,"column":5},"action":"insert","lines":["l"]},{"start":{"row":10,"column":5},"end":{"row":10,"column":6},"action":"insert","lines":["o"]},{"start":{"row":10,"column":6},"end":{"row":10,"column":7},"action":"insert","lines":["g"]},{"start":{"row":10,"column":7},"end":{"row":10,"column":8},"action":"insert","lines":["i"]},{"start":{"row":10,"column":8},"end":{"row":10,"column":9},"action":"insert","lines":["n"]}],[{"start":{"row":10,"column":9},"end":{"row":10,"column":11},"action":"insert","lines":["()"],"id":135}],[{"start":{"row":10,"column":11},"end":{"row":10,"column":12},"action":"insert","lines":[":"],"id":136}],[{"start":{"row":10,"column":12},"end":{"row":11,"column":0},"action":"insert","lines":["",""],"id":137},{"start":{"row":11,"column":0},"end":{"row":11,"column":4},"action":"insert","lines":["    "]},{"start":{"row":11,"column":4},"end":{"row":11,"column":5},"action":"insert","lines":["r"]},{"start":{"row":11,"column":5},"end":{"row":11,"column":6},"action":"insert","lines":["e"]},{"start":{"row":11,"column":6},"end":{"row":11,"column":7},"action":"insert","lines":["u"]},{"start":{"row":11,"column":7},"end":{"row":11,"column":8},"action":"insert","lines":["t"]}],[{"start":{"row":11,"column":7},"end":{"row":11,"column":8},"action":"remove","lines":["t"],"id":138},{"start":{"row":11,"column":6},"end":{"row":11,"column":7},"action":"remove","lines":["u"]}],[{"start":{"row":11,"column":6},"end":{"row":11,"column":7},"action":"insert","lines":["t"],"id":139},{"start":{"row":11,"column":7},"end":{"row":11,"column":8},"action":"insert","lines":["i"]},{"start":{"row":11,"column":8},"end":{"row":11,"column":9},"action":"insert","lines":["r"]}],[{"start":{"row":11,"column":8},"end":{"row":11,"column":9},"action":"remove","lines":["r"],"id":140},{"start":{"row":11,"column":7},"end":{"row":11,"column":8},"action":"remove","lines":["i"]}],[{"start":{"row":11,"column":7},"end":{"row":11,"column":8},"action":"insert","lines":["u"],"id":141},{"start":{"row":11,"column":8},"end":{"row":11,"column":9},"action":"insert","lines":["r"]},{"start":{"row":11,"column":9},"end":{"row":11,"column":10},"action":"insert","lines":["n"]}],[{"start":{"row":11,"column":10},"end":{"row":11,"column":11},"action":"insert","lines":[" "],"id":142},{"start":{"row":11,"column":11},"end":{"row":11,"column":12},"action":"insert","lines":["r"]},{"start":{"row":11,"column":12},"end":{"row":11,"column":13},"action":"insert","lines":["e"]},{"start":{"row":11,"column":13},"end":{"row":11,"column":14},"action":"insert","lines":["n"]},{"start":{"row":11,"column":14},"end":{"row":11,"column":15},"action":"insert","lines":["d"]},{"start":{"row":11,"column":15},"end":{"row":11,"column":16},"action":"insert","lines":["e"]},{"start":{"row":11,"column":16},"end":{"row":11,"column":17},"action":"insert","lines":["r"]}],[{"start":{"row":11,"column":11},"end":{"row":11,"column":17},"action":"remove","lines":["render"],"id":143},{"start":{"row":11,"column":11},"end":{"row":11,"column":26},"action":"insert","lines":["render_template"]}],[{"start":{"row":11,"column":26},"end":{"row":11,"column":28},"action":"insert","lines":["()"],"id":144}],[{"start":{"row":11,"column":27},"end":{"row":11,"column":29},"action":"insert","lines":["\"\""],"id":145}],[{"start":{"row":11,"column":28},"end":{"row":11,"column":29},"action":"insert","lines":["l"],"id":146},{"start":{"row":11,"column":29},"end":{"row":11,"column":30},"action":"insert","lines":["o"]},{"start":{"row":11,"column":30},"end":{"row":11,"column":31},"action":"insert","lines":["g"]},{"start":{"row":11,"column":31},"end":{"row":11,"column":32},"action":"insert","lines":["i"]},{"start":{"row":11,"column":32},"end":{"row":11,"column":33},"action":"insert","lines":["n"]},{"start":{"row":11,"column":33},"end":{"row":11,"column":34},"action":"insert","lines":["."]},{"start":{"row":11,"column":34},"end":{"row":11,"column":35},"action":"insert","lines":["h"]},{"start":{"row":11,"column":35},"end":{"row":11,"column":36},"action":"insert","lines":["t"]},{"start":{"row":11,"column":36},"end":{"row":11,"column":37},"action":"insert","lines":["m"]}],[{"start":{"row":11,"column":37},"end":{"row":11,"column":38},"action":"insert","lines":["l"],"id":147}],[{"start":{"row":11,"column":38},"end":{"row":11,"column":40},"action":"insert","lines":["  "],"id":148}],[{"start":{"row":11,"column":39},"end":{"row":11,"column":40},"action":"remove","lines":[" "],"id":149},{"start":{"row":11,"column":38},"end":{"row":11,"column":39},"action":"remove","lines":[" "]}],[{"start":{"row":15,"column":42},"end":{"row":16,"column":0},"action":"insert","lines":["",""],"id":150},{"start":{"row":16,"column":0},"end":{"row":16,"column":4},"action":"insert","lines":["    "]},{"start":{"row":16,"column":4},"end":{"row":17,"column":0},"action":"insert","lines":["",""]},{"start":{"row":17,"column":0},"end":{"row":17,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":17,"column":0},"end":{"row":17,"column":4},"action":"remove","lines":["    "],"id":151}],[{"start":{"row":17,"column":0},"end":{"row":17,"column":1},"action":"insert","lines":["@"],"id":152},{"start":{"row":17,"column":1},"end":{"row":17,"column":2},"action":"insert","lines":["a"]},{"start":{"row":17,"column":2},"end":{"row":17,"column":3},"action":"insert","lines":["p"]},{"start":{"row":17,"column":3},"end":{"row":17,"column":4},"action":"insert","lines":["p"]}],[{"start":{"row":17,"column":4},"end":{"row":17,"column":5},"action":"insert","lines":["."],"id":153},{"start":{"row":17,"column":5},"end":{"row":17,"column":6},"action":"insert","lines":["r"]},{"start":{"row":17,"column":6},"end":{"row":17,"column":7},"action":"insert","lines":["o"]},{"start":{"row":17,"column":7},"end":{"row":17,"column":8},"action":"insert","lines":["y"]}],[{"start":{"row":17,"column":7},"end":{"row":17,"column":8},"action":"remove","lines":["y"],"id":154}],[{"start":{"row":17,"column":7},"end":{"row":17,"column":8},"action":"insert","lines":["u"],"id":155},{"start":{"row":17,"column":8},"end":{"row":17,"column":9},"action":"insert","lines":["t"]},{"start":{"row":17,"column":9},"end":{"row":17,"column":10},"action":"insert","lines":["e"]}],[{"start":{"row":17,"column":10},"end":{"row":17,"column":12},"action":"insert","lines":["()"],"id":156}],[{"start":{"row":17,"column":11},"end":{"row":17,"column":13},"action":"insert","lines":["\"\""],"id":157}],[{"start":{"row":17,"column":12},"end":{"row":17,"column":13},"action":"insert","lines":["f"],"id":158},{"start":{"row":17,"column":13},"end":{"row":17,"column":14},"action":"insert","lines":["a"]},{"start":{"row":17,"column":14},"end":{"row":17,"column":15},"action":"insert","lines":["v"]}],[{"start":{"row":17,"column":14},"end":{"row":17,"column":15},"action":"remove","lines":["v"],"id":159},{"start":{"row":17,"column":13},"end":{"row":17,"column":14},"action":"remove","lines":["a"]},{"start":{"row":17,"column":12},"end":{"row":17,"column":13},"action":"remove","lines":["f"]}],[{"start":{"row":17,"column":12},"end":{"row":17,"column":13},"action":"insert","lines":["/"],"id":160},{"start":{"row":17,"column":13},"end":{"row":17,"column":14},"action":"insert","lines":["f"]},{"start":{"row":17,"column":14},"end":{"row":17,"column":15},"action":"insert","lines":["a"]},{"start":{"row":17,"column":15},"end":{"row":17,"column":16},"action":"insert","lines":["v"]},{"start":{"row":17,"column":16},"end":{"row":17,"column":17},"action":"insert","lines":["o"]},{"start":{"row":17,"column":17},"end":{"row":17,"column":18},"action":"insert","lines":["u"]},{"start":{"row":17,"column":18},"end":{"row":17,"column":19},"action":"insert","lines":["r"]},{"start":{"row":17,"column":19},"end":{"row":17,"column":20},"action":"insert","lines":["i"]},{"start":{"row":17,"column":20},"end":{"row":17,"column":21},"action":"insert","lines":["t"]},{"start":{"row":17,"column":21},"end":{"row":17,"column":22},"action":"insert","lines":["e"]}],[{"start":{"row":17,"column":22},"end":{"row":17,"column":23},"action":"insert","lines":["s"],"id":161}],[{"start":{"row":17,"column":25},"end":{"row":18,"column":0},"action":"insert","lines":["",""],"id":162},{"start":{"row":18,"column":0},"end":{"row":18,"column":1},"action":"insert","lines":["d"]},{"start":{"row":18,"column":1},"end":{"row":18,"column":2},"action":"insert","lines":["e"]},{"start":{"row":18,"column":2},"end":{"row":18,"column":3},"action":"insert","lines":["f"]}],[{"start":{"row":18,"column":3},"end":{"row":18,"column":4},"action":"insert","lines":[" "],"id":163},{"start":{"row":18,"column":4},"end":{"row":18,"column":5},"action":"insert","lines":["f"]},{"start":{"row":18,"column":5},"end":{"row":18,"column":6},"action":"insert","lines":["a"]},{"start":{"row":18,"column":6},"end":{"row":18,"column":7},"action":"insert","lines":["v"]},{"start":{"row":18,"column":7},"end":{"row":18,"column":8},"action":"insert","lines":["o"]},{"start":{"row":18,"column":8},"end":{"row":18,"column":9},"action":"insert","lines":["u"]},{"start":{"row":18,"column":9},"end":{"row":18,"column":10},"action":"insert","lines":["r"]}],[{"start":{"row":18,"column":10},"end":{"row":18,"column":11},"action":"insert","lines":["i"],"id":164},{"start":{"row":18,"column":11},"end":{"row":18,"column":12},"action":"insert","lines":["t"]},{"start":{"row":18,"column":12},"end":{"row":18,"column":13},"action":"insert","lines":["e"]},{"start":{"row":18,"column":13},"end":{"row":18,"column":14},"action":"insert","lines":["s"]}],[{"start":{"row":18,"column":14},"end":{"row":18,"column":15},"action":"insert","lines":[":"],"id":165}],[{"start":{"row":18,"column":14},"end":{"row":18,"column":15},"action":"remove","lines":[":"],"id":166}],[{"start":{"row":18,"column":14},"end":{"row":18,"column":16},"action":"insert","lines":["()"],"id":167}],[{"start":{"row":18,"column":16},"end":{"row":18,"column":17},"action":"insert","lines":[":"],"id":168}],[{"start":{"row":18,"column":17},"end":{"row":19,"column":0},"action":"insert","lines":["",""],"id":169},{"start":{"row":19,"column":0},"end":{"row":19,"column":4},"action":"insert","lines":["    "]},{"start":{"row":19,"column":4},"end":{"row":19,"column":5},"action":"insert","lines":["r"]},{"start":{"row":19,"column":5},"end":{"row":19,"column":6},"action":"insert","lines":["e"]},{"start":{"row":19,"column":6},"end":{"row":19,"column":7},"action":"insert","lines":["t"]},{"start":{"row":19,"column":7},"end":{"row":19,"column":8},"action":"insert","lines":["u"]},{"start":{"row":19,"column":8},"end":{"row":19,"column":9},"action":"insert","lines":["r"]},{"start":{"row":19,"column":9},"end":{"row":19,"column":10},"action":"insert","lines":["n"]}],[{"start":{"row":19,"column":10},"end":{"row":19,"column":11},"action":"insert","lines":[" "],"id":170},{"start":{"row":19,"column":11},"end":{"row":19,"column":12},"action":"insert","lines":["e"]}],[{"start":{"row":19,"column":11},"end":{"row":19,"column":12},"action":"remove","lines":["e"],"id":171}],[{"start":{"row":19,"column":11},"end":{"row":19,"column":12},"action":"insert","lines":["r"],"id":172},{"start":{"row":19,"column":12},"end":{"row":19,"column":13},"action":"insert","lines":["e"]},{"start":{"row":19,"column":13},"end":{"row":19,"column":14},"action":"insert","lines":["n"]},{"start":{"row":19,"column":14},"end":{"row":19,"column":15},"action":"insert","lines":["d"]},{"start":{"row":19,"column":15},"end":{"row":19,"column":16},"action":"insert","lines":["e"]}],[{"start":{"row":19,"column":11},"end":{"row":19,"column":16},"action":"remove","lines":["rende"],"id":173},{"start":{"row":19,"column":11},"end":{"row":19,"column":26},"action":"insert","lines":["render_template"]}],[{"start":{"row":19,"column":26},"end":{"row":19,"column":28},"action":"insert","lines":["()"],"id":174}],[{"start":{"row":19,"column":27},"end":{"row":19,"column":29},"action":"insert","lines":["\"\""],"id":175}],[{"start":{"row":19,"column":28},"end":{"row":19,"column":29},"action":"insert","lines":["f"],"id":176},{"start":{"row":19,"column":29},"end":{"row":19,"column":30},"action":"insert","lines":["a"]},{"start":{"row":19,"column":30},"end":{"row":19,"column":31},"action":"insert","lines":["v"]},{"start":{"row":19,"column":31},"end":{"row":19,"column":32},"action":"insert","lines":["o"]},{"start":{"row":19,"column":32},"end":{"row":19,"column":33},"action":"insert","lines":["u"]},{"start":{"row":19,"column":33},"end":{"row":19,"column":34},"action":"insert","lines":["r"]},{"start":{"row":19,"column":34},"end":{"row":19,"column":35},"action":"insert","lines":["i"]},{"start":{"row":19,"column":35},"end":{"row":19,"column":36},"action":"insert","lines":["t"]},{"start":{"row":19,"column":36},"end":{"row":19,"column":37},"action":"insert","lines":["e"]},{"start":{"row":19,"column":37},"end":{"row":19,"column":38},"action":"insert","lines":["s"]}],[{"start":{"row":19,"column":38},"end":{"row":19,"column":39},"action":"insert","lines":["."],"id":177},{"start":{"row":19,"column":39},"end":{"row":19,"column":40},"action":"insert","lines":["h"]},{"start":{"row":19,"column":40},"end":{"row":19,"column":41},"action":"insert","lines":["t"]},{"start":{"row":19,"column":41},"end":{"row":19,"column":42},"action":"insert","lines":["m"]},{"start":{"row":19,"column":42},"end":{"row":19,"column":43},"action":"insert","lines":["l"]}],[{"start":{"row":12,"column":0},"end":{"row":34,"column":8},"action":"insert","lines":["# New user registration template.","@app.route('/new_user')","def new_user():","    return render_template('new_user.html')  ","","# New user registration submit","@app.route('/new_user/register', methods=['GET','POST'])","def register():","    user={}","    users=mongo.db.users","    username=request.form['user']","    # It checks if the user name is not being used before","    if users.find_one({\"user\":username}):","        flash('Username invalid, already in use.')","        return redirect(url_for('new_user'))","    else: ","        # User name valid as new user, redirecting to the login page","        user[\"user\"]=username","        user[\"password\"]=request.form['password']","        users.insert_one(user)","        flash('User created. You can now login.')","        return redirect(url_for('autentication'))","        "],"id":178}],[{"start":{"row":11,"column":40},"end":{"row":12,"column":0},"action":"insert","lines":["",""],"id":179},{"start":{"row":12,"column":0},"end":{"row":12,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":8,"column":3},"end":{"row":9,"column":0},"action":"insert","lines":["",""],"id":180},{"start":{"row":9,"column":0},"end":{"row":9,"column":3},"action":"insert","lines":["   "]}],[{"start":{"row":9,"column":2},"end":{"row":9,"column":3},"action":"remove","lines":[" "],"id":181},{"start":{"row":9,"column":1},"end":{"row":9,"column":2},"action":"remove","lines":[" "]},{"start":{"row":9,"column":0},"end":{"row":9,"column":1},"action":"remove","lines":[" "]}],[{"start":{"row":8,"column":3},"end":{"row":9,"column":1},"action":"remove","lines":[""," "],"id":182}],[{"start":{"row":8,"column":3},"end":{"row":9,"column":0},"action":"insert","lines":["",""],"id":183},{"start":{"row":9,"column":0},"end":{"row":9,"column":3},"action":"insert","lines":["   "]}],[{"start":{"row":2,"column":0},"end":{"row":3,"column":0},"action":"insert","lines":["",""],"id":184}],[{"start":{"row":2,"column":0},"end":{"row":3,"column":34},"action":"insert","lines":["from flask_pymongo import PyMongo","from bson.objectid import ObjectId"],"id":185}],[{"start":{"row":29,"column":24},"end":{"row":29,"column":47},"action":"remove","lines":["invalid, already in use"],"id":186},{"start":{"row":29,"column":24},"end":{"row":29,"column":25},"action":"insert","lines":["n"]},{"start":{"row":29,"column":25},"end":{"row":29,"column":26},"action":"insert","lines":["o"]},{"start":{"row":29,"column":26},"end":{"row":29,"column":27},"action":"insert","lines":["t"]}],[{"start":{"row":29,"column":27},"end":{"row":29,"column":28},"action":"insert","lines":[" "],"id":187},{"start":{"row":29,"column":28},"end":{"row":29,"column":29},"action":"insert","lines":["v"]},{"start":{"row":29,"column":29},"end":{"row":29,"column":30},"action":"insert","lines":["a"]},{"start":{"row":29,"column":30},"end":{"row":29,"column":31},"action":"insert","lines":["l"]},{"start":{"row":29,"column":31},"end":{"row":29,"column":32},"action":"insert","lines":["i"]},{"start":{"row":29,"column":32},"end":{"row":29,"column":33},"action":"insert","lines":["d"]},{"start":{"row":29,"column":33},"end":{"row":29,"column":34},"action":"insert","lines":[","]}],[{"start":{"row":29,"column":34},"end":{"row":29,"column":35},"action":"insert","lines":[" "],"id":188},{"start":{"row":29,"column":35},"end":{"row":29,"column":36},"action":"insert","lines":["a"]},{"start":{"row":29,"column":36},"end":{"row":29,"column":37},"action":"insert","lines":["l"]},{"start":{"row":29,"column":37},"end":{"row":29,"column":38},"action":"insert","lines":["r"]},{"start":{"row":29,"column":38},"end":{"row":29,"column":39},"action":"insert","lines":["e"]}],[{"start":{"row":29,"column":39},"end":{"row":29,"column":40},"action":"insert","lines":["a"],"id":189},{"start":{"row":29,"column":40},"end":{"row":29,"column":41},"action":"insert","lines":["d"]},{"start":{"row":29,"column":41},"end":{"row":29,"column":42},"action":"insert","lines":["y"]}],[{"start":{"row":29,"column":42},"end":{"row":29,"column":43},"action":"insert","lines":[" "],"id":190},{"start":{"row":29,"column":43},"end":{"row":29,"column":44},"action":"insert","lines":["t"]},{"start":{"row":29,"column":44},"end":{"row":29,"column":45},"action":"insert","lines":["a"]},{"start":{"row":29,"column":45},"end":{"row":29,"column":46},"action":"insert","lines":["k"]},{"start":{"row":29,"column":46},"end":{"row":29,"column":47},"action":"insert","lines":["e"]}],[{"start":{"row":29,"column":47},"end":{"row":29,"column":48},"action":"insert","lines":["n"],"id":191}],[{"start":{"row":1,"column":40},"end":{"row":1,"column":84},"action":"insert","lines":[", redirect, request, url_for, session, flash"],"id":192}],[{"start":{"row":5,"column":21},"end":{"row":6,"column":0},"action":"insert","lines":["",""],"id":193},{"start":{"row":6,"column":0},"end":{"row":7,"column":0},"action":"insert","lines":["",""]}],[{"start":{"row":7,"column":0},"end":{"row":7,"column":18},"action":"insert","lines":["mongo=PyMongo(app)"],"id":194}],[{"start":{"row":5,"column":21},"end":{"row":6,"column":0},"action":"insert","lines":["",""],"id":195}],[{"start":{"row":6,"column":0},"end":{"row":7,"column":37},"action":"insert","lines":["app.secret_key = os.getenv(\"SECRET_KEY\")","app.config[\"MONGO_DBNAME\"]=\"CookBook\""],"id":196}],[{"start":{"row":7,"column":37},"end":{"row":8,"column":0},"action":"insert","lines":["",""],"id":197}],[{"start":{"row":8,"column":0},"end":{"row":8,"column":48},"action":"insert","lines":["app.config[\"MONGO_URI\"]=os.getenv(\"MONGODB_URI\")"],"id":198}],[{"start":{"row":8,"column":45},"end":{"row":8,"column":46},"action":"remove","lines":["I"],"id":199},{"start":{"row":8,"column":44},"end":{"row":8,"column":45},"action":"remove","lines":["R"]},{"start":{"row":8,"column":43},"end":{"row":8,"column":44},"action":"remove","lines":["U"]},{"start":{"row":8,"column":42},"end":{"row":8,"column":43},"action":"remove","lines":["_"]},{"start":{"row":8,"column":41},"end":{"row":8,"column":42},"action":"remove","lines":["B"]},{"start":{"row":8,"column":40},"end":{"row":8,"column":41},"action":"remove","lines":["D"]},{"start":{"row":8,"column":39},"end":{"row":8,"column":40},"action":"remove","lines":["O"]},{"start":{"row":8,"column":38},"end":{"row":8,"column":39},"action":"remove","lines":["G"]},{"start":{"row":8,"column":37},"end":{"row":8,"column":38},"action":"remove","lines":["N"]},{"start":{"row":8,"column":36},"end":{"row":8,"column":37},"action":"remove","lines":["O"]},{"start":{"row":8,"column":35},"end":{"row":8,"column":36},"action":"remove","lines":["M"]}],[{"start":{"row":8,"column":35},"end":{"row":8,"column":147},"action":"insert","lines":["mongodb+srv://Debbiepimpo:Nora171215@my-first-cluster-gsys1.mongodb.net/task-manager?retryWrites=true&w=majority"],"id":200}],[{"start":{"row":8,"column":112},"end":{"row":8,"column":119},"action":"remove","lines":["manager"],"id":201},{"start":{"row":8,"column":111},"end":{"row":8,"column":112},"action":"remove","lines":["-"]},{"start":{"row":8,"column":110},"end":{"row":8,"column":111},"action":"remove","lines":["k"]},{"start":{"row":8,"column":109},"end":{"row":8,"column":110},"action":"remove","lines":["s"]},{"start":{"row":8,"column":108},"end":{"row":8,"column":109},"action":"remove","lines":["a"]},{"start":{"row":8,"column":107},"end":{"row":8,"column":108},"action":"remove","lines":["t"]}],[{"start":{"row":8,"column":107},"end":{"row":8,"column":108},"action":"insert","lines":["C"],"id":202},{"start":{"row":8,"column":108},"end":{"row":8,"column":109},"action":"insert","lines":["o"]},{"start":{"row":8,"column":109},"end":{"row":8,"column":110},"action":"insert","lines":["o"]},{"start":{"row":8,"column":110},"end":{"row":8,"column":111},"action":"insert","lines":["k"]}],[{"start":{"row":8,"column":111},"end":{"row":8,"column":112},"action":"insert","lines":["B"],"id":203},{"start":{"row":8,"column":112},"end":{"row":8,"column":113},"action":"insert","lines":["o"]},{"start":{"row":8,"column":113},"end":{"row":8,"column":114},"action":"insert","lines":["o"]},{"start":{"row":8,"column":114},"end":{"row":8,"column":115},"action":"insert","lines":["k"]}],[{"start":{"row":8,"column":35},"end":{"row":8,"column":143},"action":"remove","lines":["mongodb+srv://Debbiepimpo:Nora171215@my-first-cluster-gsys1.mongodb.net/CookBook?retryWrites=true&w=majority"],"id":207}],[{"start":{"row":8,"column":35},"end":{"row":8,"column":36},"action":"insert","lines":["M"],"id":208},{"start":{"row":8,"column":36},"end":{"row":8,"column":37},"action":"insert","lines":["o"]},{"start":{"row":8,"column":37},"end":{"row":8,"column":38},"action":"insert","lines":["n"]}],[{"start":{"row":8,"column":37},"end":{"row":8,"column":38},"action":"remove","lines":["n"],"id":209},{"start":{"row":8,"column":36},"end":{"row":8,"column":37},"action":"remove","lines":["o"]}],[{"start":{"row":8,"column":36},"end":{"row":8,"column":37},"action":"insert","lines":["O"],"id":210},{"start":{"row":8,"column":37},"end":{"row":8,"column":38},"action":"insert","lines":["N"]},{"start":{"row":8,"column":38},"end":{"row":8,"column":39},"action":"insert","lines":["G"]},{"start":{"row":8,"column":39},"end":{"row":8,"column":40},"action":"insert","lines":["O"]}],[{"start":{"row":8,"column":40},"end":{"row":8,"column":41},"action":"insert","lines":["_"],"id":211}],[{"start":{"row":8,"column":41},"end":{"row":8,"column":42},"action":"insert","lines":["U"],"id":212},{"start":{"row":8,"column":42},"end":{"row":8,"column":43},"action":"insert","lines":["R"]},{"start":{"row":8,"column":43},"end":{"row":8,"column":44},"action":"insert","lines":["I"]}],[{"start":{"row":8,"column":40},"end":{"row":8,"column":41},"action":"insert","lines":["s"],"id":213}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":22,"column":23},"end":{"row":22,"column":23},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1565616009922}