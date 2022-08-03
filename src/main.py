import sys
import spotify
import util

if __name__ == "__main__":
    args = sys.argv
    args.pop(0)
    arg_count = len(args)

    if arg_count == 0:
        exit(
"""
    Anpu (暗譜)

usage: anpu <options> <query>
       anpu <link>

Options:
    --limit, -l                    Set the query limit (default=10).
    --track, -t                    Set search query type for tracks (default).
    --album, -a                    Set search query type for albums.
"""
        )

    client = spotify.client()

    link = args[arg_count - 1]

    if any(x in link for x in ("http", "www")):
        util.print_indented(client.search_link(link))
    else:
        query_type = "track"
        query_limit = 10

        opt_idx = []

        type_opts = {
            "--track": "track",
            "-t": "track",
            "--album": "album",
            "-a": "album",
        }

        for opt in args:
            idx = args.index(opt)

            for k in type_opts:
                if opt == k:
                    opt_idx.append(idx)
                    query_type = type_opts[k]

            if opt == "--limit" or opt == "-l":
                opt_idx.append(idx)

                try:
                    query_limit = int(args[idx + 1])
                    opt_idx.append(idx + 1)
                except:
                    exit("You didn't specify a limit.")

        query = []

        for x in args:
            if args.index(x) in opt_idx:
                continue

            query.append(x)

        query = " ".join(x for x in query)

        util.print_indented(client.search_query({
            "q": query,
            "type": query_type,
            "limit": query_limit}))

