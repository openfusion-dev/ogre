#!/usr/bin/python


def get(kinds, sources, relations):
    """Get local or recent media from a public source and return a dictionary.

    kinds     -- a tuple of content mediums to get
    sources   -- a tuple of sources to get content from
    relations -- a dictionary of 2-tuples specifying
                 a location or time and a radius

    """
    for kind in kinds:
        if kind.lower() not in ["image", "sound", "text", "video"]:
            print "invalid kind", kind
            return
    for source in sources:
        if source.lower() not in ["twitter"]:
            print "invalid source", source
            return
    for relation in relations.keys():
        if relation.lower() not in ["location", "time"]:
            print "invalid relation", relation
            return
    pass  # TODO Call the appropriate handler based on parameters.
    return
