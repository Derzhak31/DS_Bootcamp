def read_and_write(file_in, file_out):
    with open(file_in, "r") as in_f:
        data = ""
        for i in in_f.readlines():
            data += (
                i.replace('","', '"\t"', 2)
                .replace('",false', '"\tfalse')
                .replace('",true', '"\ttrue')
                .replace("false,", "false\t")
                .replace("true,", "true\t")
            )
        with open(file_out, "w") as out_f:
            out_f.writelines(data)


if __name__ == "__main__":
    input_file = "ds.csv"
    output_file = "ds.tsv"
    read_and_write(input_file, output_file)
