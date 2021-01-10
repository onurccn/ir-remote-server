import json

from flask import request, abort, jsonify

from app import app, db
from app.models import Remote, Command


@app.route("/")
def index():
    return "Hello world..."


@app.route("/remote", methods=['POST'])
def addRemote():
    if not request.is_json:
        return 'Body not valid', 405

    remoteDict = request.get_json()
    name = remoteDict['name']
    commands = []
    for commandDict in remoteDict['commands']:
        commands.append(parseCommand(commandDict))

    remote = Remote(name, commands)
    db.session.add(remote)
    db.session.commit()

    return jsonify(serializeRemote(remote))


@app.route("/remote", methods=['GET'])
def getRemotes():
    remotes = Remote.query.all()
    remotesDict = []
    for remote in remotes:
        remoteDict = serializeRemote(remote)
        remotesDict.append(remoteDict)
    return jsonify(remotesDict)


@app.route("/remote/<remoteFilter>", methods=['GET'])
def getRemote(remoteFilter):
    try:
        remoteFilter = int(remoteFilter)
    except:
        pass

    remote = None
    if isinstance(remoteFilter, str):
        remote = Remote.query.filter_by(name=remoteFilter).first()
    elif isinstance(remoteFilter, int):
        remote = Remote.query.filter_by(id=remoteFilter).first()
    else:
        abort(500)

    if not remote:
        abort(404)

    remoteDict = serializeRemote(remote)
    return jsonify(remoteDict)


@app.route("/remote", methods=['DELETE'])
def deleteAll():
    deletedCommands = Command.query.delete()
    deletedRemotes = Remote.query.delete()
    db.session.commit()
    return jsonify({'deletedCommands': deletedCommands, 'deletedRemotes': deletedRemotes})


@app.route("/command", methods=['POST'])
def addCommand():
    if not request.is_json:
        return 'Body not valid', 405

    remoteDict = request.get_json()

    command = parseCommand(remoteDict['command'])
    command.remote_id = -1
    if 'remoteId' in remoteDict:
        command.remote_id = remoteDict['remoteId']
    elif 'remoteName' in remoteDict:
        remote = Remote.query.filter_by(name=remoteDict['remoteName']).first()
        if remote:
            command.remote_id = remote.id

    if command.remote_id < 1:
        abort(404)

    db.session.add(command)
    db.session.commit()

    return jsonify(serializeCommand(command))


def serializeRemote(remote):
    remoteDict = {
        'id': remote.id,
        'name': remote.name,
        'commands': []
    }

    for command in remote.commands:
        remoteDict['commands'].append(serializeCommand(command))

    return remoteDict


def serializeCommand(command):
    return {
        'id': command.id,
        'name': command.name,
        'decode_type': command.decodeType,
        'value': command.value,
        'raw': command.raw.split(","),
        'rawLen': command.rawLen,
        'bitLen': command.bitLen,
        'pos': command.position
    }


def parseCommand(commandDict):
    name = commandDict['name']
    decodeType = commandDict['decode_type']
    value = commandDict['value']
    rawLen = commandDict['rawLen']
    bitLen = commandDict['bitLen']
    raw = ",".join([str(val) for val in commandDict['raw']])
    pos = commandDict['pos']

    return Command(name, decodeType, value, raw, rawLen, bitLen, pos)
