import os, json, asyncio, configparser, random
from quart import Quart, render_template, url_for, flash, redirect, request, abort, jsonify, send_file
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import afs_memory as afs
from datetime import datetime

dashboard = Quart(__name__)
__maintainer__ = "Atae Kurri <hakussura@protonmail.com>"
dashboard.config['SECRET_KEY'] = 'ba41339cd8869fcf8608937a5c4eb79812'
dashboard.config["DISCORD_CLIENT_ID"] = 746348869574459472
dashboard.config["DISCORD_CLIENT_SECRET"] = "CS-Lv5JPoEn6gFUrrCT3sp1iedt3Mzw3"
dashboard.config["DISCORD_REDIRECT_URI"] = "http://localhost/"
dashboard.config["DISCORD_BOT_TOKEN"] = open("././token.txt").read()

discord = DiscordOAuth2Session(dashboard)

dashboard.static_folder = 'static'

def store_activities(data):
    with open("././json/activities.json", 'r') as f:
        act = json.load(f)

    data["date"] = datetime.now().strftime('%A %B at %H:%M')
    r = str(random.randint(0, 99999))
    while r in act:
        r = str(random.randint(0, 99999))
    act[r] = data
    with open("././json/activities.json", 'w') as f:
        json.dump(act, f, indent=2)

#@dashboard.context_processor
#def utility_processor():
#    def toggle_serv_conf(value, guild_id):
#        c_f = afs.afs_memory("././db.afs")
#        conf = c_f.j_load # load conf
#        # Il faut que je redige vers une page tampon qui va changer la valeur et me rediriger vers la page de la guild
#        if value == "interphone":
#            if conf["serverconfig"][guild_id]["interphone"]:
#                conf["serverconfig"][guild_id]["interphone"] = False
#                c_f.write_json_to_afs(c_f.j_load, conf)
#            else:
#                conf["serverconfig"][guild_id]["interphone"] = True
#                c_f.write_json_to_afs(c_f.j_load, conf)
#    return dict(toggle_serv_conf=toggle_serv_conf)

@dashboard.route('/')
async def home():
    c_f = afs.afs_memory("././db.afs")
    conf = c_f.j_load # load conf
    # Gestion de l'ordre et du nombre d'activités à afficher
    with open("././json/activities.json", 'r') as f:
        act = json.load(f)
    act = dict(reversed(list(act.items())))
    activities = {}
    i = 0
    for a in act:
        if i < 5:
            activities[i] = act[a]
        i = i+1
    # Gestion de la liaison de l'image de la guild par rapport à son dans conf
    for guild in activities:
        name = activities[guild]["g_name"]
        for key, value in conf["serverconfig"].items():
            if conf["serverconfig"][key]["name"] == name:
                k = key
        activities[guild]["icon_url"] = conf["serverconfig"][k]["icon_url"]
    return await render_template('home.html', title="Dashboard", servs=conf["serverconfig"], activities=activities)

@dashboard.route("/login/")
async def login():
    return await discord.create_session()

@dashboard.route("/callback/")
async def callback():
    await discord.callback()
    return redirect(url_for("home"))
    
@dashboard.errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("login"))

@dashboard.route('/guild', methods=['GET', 'POST'])
async def guild():
    if request.method == "GET":
        guild_id = request.args.get('guild_id', None, type=str)
        c_f = afs.afs_memory("././db.afs")
        conf = c_f.j_load # load conf
        guild = conf["serverconfig"][guild_id]
        cmds = ', '.join(guild["cmds"]) or "Aucune"

        con = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]}, allow_no_value=True)
        con.read("././config.ini")
        listcmds = con["variables"].getlist("Togglable_cmds")
        return await render_template('guild.html', guild=guild, guild_id=guild_id, cmds=cmds, listcmds=listcmds)

@dashboard.route('/guild/toggle_interphone', methods=['GET', 'POST'])
async def toggle_interphone():
    if request.method == "GET":
        guild_id = request.args.get('guild_id', None, type=str)
        c_f = afs.afs_memory("././db.afs")
        conf = c_f.j_load # load conf
        # Il faut que je redige vers une page tampon qui va changer la valeur et me rediriger vers la page de la guild
        if conf["serverconfig"][guild_id]["interphone"]:
            conf["serverconfig"][guild_id]["interphone"] = False
            conf["serverconfig"][guild_id]["cmds"]["phone"] = "phone"
            c_f.write_json_to_afs(c_f.j_load, conf)
        else:
            conf["serverconfig"][guild_id]["interphone"] = True
            c_f.write_json_to_afs(c_f.j_load, conf)
            c_f.delete_json_from_afs(conf, f"serverconfig.{guild_id}.cmds.phone")
        return redirect(url_for('guild', guild_id=guild_id))

@dashboard.route('/guild/toggle_cmds', methods=['GET', 'POST'])
async def toggle_cmds():
    guild_id = request.args.get('guild_id', None, type=str)
    cmd = request.args.get('cmd', None, type=str)
    c_f = afs.afs_memory("././db.afs")
    conf = c_f.j_load

    if cmd in conf["serverconfig"][guild_id]["cmds"]:
        c_f.delete_json_from_afs(conf, f"serverconfig.{guild_id}.cmds.{cmd}")
    else:
        conf["serverconfig"][guild_id]["cmds"][cmd] = cmd
        c_f.write_json_to_afs(c_f.j_load, conf)
    return redirect(url_for('guild', guild_id=guild_id))

@dashboard.route('/guild/change_lang', methods=['GET'])
async def change_lang():
    guild_id = request.args.get('guild_id', None, type=str)
    lang = request.args.get('lang', None, type=str)

    c_f = afs.afs_memory("././db.afs")
    conf = c_f.j_load

    conf["serverconfig"][guild_id]["lang"] = lang
    c_f.write_json_to_afs(c_f.j_load, conf)

    store_activities({
            "g_name": conf["serverconfig"][guild_id]["name"],
            "cmd": "setLang",
            "desc": f"Langue changée pour {lang}. Dashboard edit."
    })

    return redirect(url_for('guild', guild_id=guild_id))

@dashboard.route('/cmds')
async def cmds():
    return await render_template('cmds.html', title="Commandes")

dashboard.run(debug=True, host="0.0.0.0", port="80")