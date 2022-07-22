from sqllineage.runner import LineageRunner


class Lineage:
    def __init__(self, sql):
        self.sql = sql

    def extract_table_level_lineage(self):
        tab_lineage = LineageRunner(self.sql)
        tab_lineage.print_table_lineage()
        return tab_lineage

    def extract_column_level_lineage(self):
        col_lineage = LineageRunner(self.sql)
        col_lineage.print_column_lineage()
        return col_lineage

    def draw_lineage_graph(self):
        LineageRunner(self.sql).draw()


if __name__ == f'__main__':
    sql_command = f'insert into circuits (circuitref, name) \
                    select column_ref, column_name from circuit_details '
    lineage_obj = Lineage(sql=sql_command)

    table_lineage = lineage_obj.extract_table_level_lineage()
    column_lineage = lineage_obj.extract_column_level_lineage()

    print(f'Table level lineage : {table_lineage}')
    print(f'Column level lineage : {column_lineage}')
    lineage_obj.draw_lineage_graph()
