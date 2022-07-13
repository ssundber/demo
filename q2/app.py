from flask import Flask, Response, request
from http import HTTPStatus
import json
import datetime

filepath = "csvinfo.csv"

app = Flask(__name__)

# Stolen from django code stuff with slight change to the results dict generated.
def parse_file(fpath):
    """
    parse "csv" file to be used in return values for Q1/Q2 of assignment.
    :param fpath: path to the file to read.
    :return: list of results as dictionaries.
    """
    outL = []
    # fpath is a csv type file with a header line.
    with open(fpath) as r:
        # Since this input file is small we're not going to bother with pandas to pull stuff out.
        # With a larger input we'd be getting this stuff out of an API that queries a DB, \
        # or perhaps querying the DB ourself so simple reading of the file should suffice here.
        for line in r:
            # The assignment shows the sample data being mostly tabs so we just split on the tab and throw out anything empty to get our elements.
            splits = [i.strip() for i in line.split("\t") if i.strip()!=""]
            if len(splits) == 3:
                outL.append({"filename":splits[0],"filepath":splits[1],"filesize":splits[2]})
    if len(outL) == 0:
        return []
    # We don't want the headerline included in the return so toss it out
    return outL[1:]




@app.route("/api/search", methods=["GET"])
def process():
    q = request.args.get('q', "")
    status_code = HTTPStatus.PROCESSING
    outD = {}
    try:
        if "filename" in q.split(":")[0]:
            # I know that ":" isn't valid in a filename, but I've been handed errors from users caused by \
            # illegal filenames before so I'm going to preserve the use supplide filename as best I can.
            # i.e. if the curl had "q=filename:testA:testB" we want fileMatch to be "testA:testB" even if it makes no sense from an OS filename point of view.
            fileMatch = ":".join(q.split(":")[1:])
            matches = []
            file_info = parse_file(filepath)
            for file in file_info:
                # Q1 just says all results matching name, not starting with and no mention of case sensitivity \
                # so a string in string check is all that we're doing.
                if fileMatch in file["name"]:
                    matches.append(file)
            # Without the datetime.timezone.utc bit we wouldn't get the +00:00 as listed in the sample output.
            outD["created"] = str(datetime.datetime.now(datetime.timezone.utc))
            outD["output"] = matches
            status_code = HTTPStatus.OK
        else:
            # We're going to keep the error message vauge because I don't know how widespread this Flask App might be.
            outD["Reson"] = "Malformed request, parameter not found."
            status_code = HTTPStatus.BAD_REQUEST
        # I know the requirements didn't ask for status info or anything but it prob should be part of an API response if this were used outside of a curl command.
        res = Response(json.dumps(outD), status=status_code,
                        mimetype='application/json')
    except Exception:
        ##TODO add logging line here (and as "as e" to the except line above).
        outD["Reson"] = "Malformed request, parameter not found."
        status_code = HTTPStatus.BAD_REQUEST
    return res
