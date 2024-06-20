import dlt
import humanize
import os


def run(s):

    # run pipeline and print results
    p = dlt.pipeline(destination="duckdb", pipeline_name="demo", dev_mode=True)
    p.run(s)

    for key, value in p.last_trace.last_normalize_info.row_counts.items():
        if key.startswith("_"):
            continue
        print(f"table {key}: {humanize.intcomma(value)} items")

    # print exraction time
    print("\n\nExtraction time")
    print(humanize.precisedelta(p.last_trace.last_extract_info.finished_at - p.last_trace.last_extract_info.started_at))
    


if __name__ == "__main__":
    os.environ["EXTRACT__NEXT_ITEM_MODE"] = "round_robin"

    @dlt.source()
    def source():

        @dlt.resource()
        def r1():
            for i in range(1000000):
                # print(f"r1 {i}")
                yield i

        @dlt.resource()
        def r2():
            for i in range(1000000):
                # print(f"r2 {i}")
                yield i

        # add limits
        r1.add_limit(max_items=10)
        r2.add_limit(max_items=10)

        return (r1, r2)

    run(source())
