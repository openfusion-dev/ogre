#!/usr/bin/python


def ogre_get(kinds, sources, relations):
    """Get local or recent media from a public source and return a dictionary.

    kinds     -- a medium of content to get
    sources   -- a source to get content from
    relations -- a dictionary of 2-tuples specifying
                 a location or time and a radius

    """
    for kind in kinds:
        kind.lower()
        if media not in ["image", "sound", "text", "video"]:
            print "invalid kind ", kind
            return
    for source in sources:
        source.lower()
        if source not in ["twitter"]:
            print "invalid source ", source
            return
    for relation in relations.keys():
        if relation not in ["location", "time"]:
            print "invalid relation ", relation
            return
    pass  # TODO Call the appropriate handler based on parameters.
    return
