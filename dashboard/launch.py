import os, json, asyncio, configparser
from quart import Quart, render_template, url_for, flash, redirect, request, abort, jsonify, send_file
from discord.ext import ipc
import afs_memory as afs

dashboard = Quart(__name__)
ipc_client = ipc.Client(
    secret_key="ba41339cd8869fcf8608937a5c4eb79812"
)
__maintainer__ = "Atae Kurri <hakussura@protonmail.com>"
#dashboard.config['SECRET_KEY'] = 'ba41339cd8869fcf8608937a5c4eb79812'
dashboard.static_folder = 'static'

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

    return redirect(url_for('guild', guild_id=guild_id))

@dashboard.route('/cmds')
async def cmds():
    return await render_template('cmds.html', title="Commandes")

dashboard.run(debug=True, host="0.0.0.0", port="80")