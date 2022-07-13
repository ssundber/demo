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
                outL.append({"name":splits[0],"path":splits[1],"size":splits[2]})
    if len(outL) == 0:
        return []
    # We don't want the headerline included in the return so toss it out
    return outL[1:]
