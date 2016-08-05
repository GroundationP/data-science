# -*- coding: UTF-8 -*-
from __future__ import division
__author__ = 'romain.jouin@gmail.com'

from    decouverte import *
import  numpy as np
import  time



def split_file_on_date(path_to_file, date_column, output_dir,  sep=';', chunksize=100000):

    import pandas as pd
    from collections import defaultdict
    import os
    assert is_file(path_to_file), "%s is not a file !"%(path)

    assert isinstance(date_column, str), "%s should be a str"%(date_column)
    if not output_dir.endswith('/'):
        output_dir = output_dir + '/'
    csv_reader = pd.read_csv(path_to_file, chunksize=chunksize, sep=sep, error_bad_lines=False)
    header_written = list()
    n = 0
    title("Reading %s"%(path_to_file))
    for df in csv_reader:
        print df[date_column]
        df['year'] = df[date_column].apply(lambda x : x[:4] if isinstance(x, str) else "-1")

        for y, v in df.groupby('year'):
            output_path = "%s%s_%s.csv"%(output_dir, get_file_name(path_to_file), str(y))
            if y not in header_written:
                title2("Beginning new file : %s" % (output_path ))
                v.to_csv(output_path , mode='a', header=True, index=False)
                header_written.append(y)
            else:
                v.to_csv(output_path , mode='a', header=False, index=False)
            n+=chunksize
            print "Read %s lines"%n

    print "%s lines written for years %s"%(n, header_written)


def do_pickle(df, x):
    import time
    import os
    import pickle
    pickle_dir_path = "/Users/nouveau/Documents/memorandum/randstad/HEC/pickles/tout_with_small_indicateurs/"
    try:
        do_pickle_in_path(df, x, pickle_dir_path)
    except:
        default = "/Users/nouveau/pickles"
        print "Attention !! \n |-> pbm picklin in [%s] \n |----> will try in [%s] "%(pickle_dir_path , default )
        do_pickle_in_path(df, x, default )

def convert_col_to_date(df, column):
    import pandas as pd
    assert isinstance(df, pd.DataFrame), "The given df is not a Dataframe, is is a [%s]."%(type(df))
    assert column in df.columns, "[%s] is not in Datframe columns (%s)"%(column, df.columns)
    from dateutil.parser import parse
    df[column] = [parse(x) for x in df[column]]
    return df


def do_pickle_in_path(df, x, pickle_dir_path):
    import os
    import pickle
    print "Going to Write down a dataframe %s"%(x)
    filename = "%s_%s"%(time.time(), x)
    save_path = os.path.join(pickle_dir_path, filename)
    df.to_csv(save_path, sep=";")
    print "%s written done in %s in [%s]"%(x, get_file_name(save_path) , pickle_dir_path)


def title(string, timeinfo=time.time()):
    import time
    print "*"*30
    print " "*int(((30-len(string)))/2), string, "(", "%s"%(time.time() - timeinfo), ")"
    print "*"*30
    return time.time()

def title2(string, timeinfo=time.time()):
    import time
    sep = "-"
    n = 40
    if "end" not in string:
        print sep*n
    print " "*int(((n-len(string))/2)), string, "(", "%s"%(time.time() - timeinfo), ")"
    if "end" in string:
        print sep*n

    return time.time()


def merge_df(df1, df2, how='left', debug=False):
    """
    Merge 2 dataframe, and display the change in size.
    :param df1: pandas dataframe
    :param df2: pandas dataframe
    :return: datframe
    """

    import pandas as pd
    assert isinstance(df1, pd.DataFrame), "DF1 is not a Pandas DataFrame, it is a [%s]"%(type(df1))
    assert isinstance(df2, pd.DataFrame), "DF2 is not a Pandas DataFrame, it is a [%s]"%(type(df2))
    how_possibilities =['left', 'right', 'outer', 'inner']
    assert how in how_possibilities , "Parameter [how] is not in %s"%(how_possibilities )
    for i in set(df1.columns).intersection( set(df2.columns)):
        pass

    new_df = pd.merge(df2,df1, how="right")#, on=i)

    assert new_df.shape[0]==df1.shape[0], "Merged from %s & %s to %s.  "%(df1.shape, df2.shape, new_df.shape)
    if debug:
        print "Merging From %s / %s to %s : %s "%(df1.shape, df2.shape, new_df.shape, new_df.columns)
    return new_df

def merge_on(df1, df2, col_df1, col_df2, how='left', debug=False):
    """
    Merge 2 dataframe, and display the change in size.
    :param df1: pandas dataframe
    :param df2: pandas dataframe
    :return: datframe
    """

    import pandas as pd
    assert isinstance(df1, pd.DataFrame), "DF1 is not a Pandas DataFrame"
    assert isinstance(df2, pd.DataFrame), "DF2 is not a Pandas DataFrame"
    try:
        unioned_df_left= pd.merge(df1                   ,
                                  df2                   ,
                                  left_on   = col_df1   ,
                                  right_on  = col_df2   ,
                                  how       = how       )
        return unioned_df_left
    except Exception as e:
        print "!! %s"%(e)


def explore_actions(file, sep=";", top = 5, k='Code Agence'):
    """
    """
    import pandas as pd
    cols     = ["MATRICULECLI","UNITE","ID_ACTION","ID_UTILISATEUR","LIB_TYPO","LIB_TYPE_ACTION","LIB_ETAT","LIB_FAMILLE","LIB_OBJECTIF","DT_DEB_ACTION","DT_FIN_ACTION","LIB_CAMPAGNE","LIB_CONTACT","LIB_CONCLUSION","FLAG_CALL_CENTER","FLAG_COMPTERENDU","FLAG_PIECEJOINTE","FLAG_RDV","NUM_COMMANDE"]
    to_check = [x for x in cols if "FLAG" in x]

    print "to_check = ", to_check

    print "Going to read : %s"%(file)
    to_explore = pd.read_csv(file, sep=";", error_bad_lines=False)
    print "to_explore.columns =", to_explore.columns

    df =pd.DataFrame()
    for col in to_check:
        serie = to_explore[col]

        if type(serie.values[0]) is str :
            try:
                values = [ int(x[0]) for x in serie.values]
                serie  = pd.Series(values, serie.index)
                to_explore[col] = serie
            except Exception as e:
                print "values = [ int(x[0]) for x in serie.values] : %s"%(e)

        else:
            print sum(serie.values)

        gpd_by_unite = to_explore.groupby("UNITE")

        if "%s"%(serie.dtype)=="object":
            print "object"
        else:
            print "-"*10
            print "%s : "%(col)
            print gpd_by_unite[col].sum()
            print gpd_by_unite[col].count()
            print gpd_by_unite[col].sum()/gpd_by_unite[col].count()
            df["nb_%s"%(col)]=gpd_by_unite[col].count()
            df["pct_%s"%(col)]=gpd_by_unite[col].sum()/gpd_by_unite[col].count()

            print "-"*10
    print "DF :"
    print df
    
def explore_2(file, sep=";", top = 5, k='Code Agence'):
    """
    """
    import pandas as pd
    cols = ["MATRICULECLI","UNITE","ID_ACTION","ID_UTILISATEUR","LIB_TYPO","LIB_TYPE_ACTION","LIB_ETAT","LIB_FAMILLE","LIB_OBJECTIF","DT_DEB_ACTION","DT_FIN_ACTION","LIB_CAMPAGNE","LIB_CONTACT","LIB_CONCLUSION","FLAG_CALL_CENTER","FLAG_COMPTERENDU","FLAG_PIECEJOINTE","FLAG_RDV","NUM_COMMANDE"]
    to_check = [x for x in cols if "FLAG" in x]

    print to_check

    print "Going to read : %s"%(file)
    to_explore = pd.read_csv(file, sep=";", error_bad_lines=False)
    print to_explore.columns

    df =pd.DataFrame()
    for col in to_check:
        serie = to_explore[col]

        if type(serie.values[0]) is str :
            try:
                values = [ int(x[0]) for x in serie.values]
                serie =pd.Series(values, serie.index)
                to_explore[col] = serie
            except Exception as e:
                print "values = [ int(x[0]) for x in serie.values] : %s"%(e)

        else:
            print sum(serie.values)

        gpd_by_unite = to_explore.groupby("UNITE")

        if "%s"%(serie.dtype)=="object":
            print "object"
        else:
            print "-"*10
            print "%s : "%(col)
            print gpd_by_unite[col].sum()
            print gpd_by_unite[col].count()
            print gpd_by_unite[col].sum()/gpd_by_unite[col].count()
            df["nb_%s"%(col)]=gpd_by_unite[col].count()
            df["pct_%s"%(col)]=gpd_by_unite[col].sum()/gpd_by_unite[col].count()

            print "-"*10
    print "DF :"
    print df

def select_items_beginning_with(array, searched_substring):
    """
    Search a substing in the array, and return the array containing the substring.

    :param array: where to search
    :param substring: searched
    :return: array
    """
    return [x for x in array if x.lower().startswith(searched_substring.lower())]


def find_mod(df, col_name, return_first_mode=True):
    """
    Return the mod of a column in a DataFrame
    :param df: Pandas dataframe
    :param col_name: string : columns from which we want the mode
    :param return_first_mode: bool if there are several modes, return all or not
    :return: array
    """
    import pandas as pd
    assert isinstance(df, pd.DataFrame), "df is not a DataFrame"
    assert col_name in df.columns, "Column is not in DataFrame"

    modes = df[col_name].mode().values
    if len(modes)>1:
        print "Attention : %s modes ! -> %s "%(len(modes), modes)

    if return_first_mode:
        return modes[0]
    return modes


def convert_serie_to_df(serie, col_handling_index):
    """
    Create a DF with two columns : one with the serie contained in the given serie,
    and a 2nd one  containing the index of the serie as column values (this col has the same value as the index of the nex df)
    :param serie: Pandas Serie to be converted
    :param col_handling_index: Name to give to the created column
    :return: Panda Dataframe
    """
    import pandas as pd
    assert isinstance(serie, pd.Series)
    df = pd.DataFrame(serie)
    df[col_handling_index]=serie.index
    return df


def find_mod_group(database, column_for_grouping, column_searched_for_mode, fill_na_with=0, create_label_column=True, create_count_column=True, create_percent_column=True):
    """
    Create a dataframe with the mode / the count of mode and the pct of mode by group of 'column_for_grouping'.
    :param database: pandas DataFrame
    :param column_for_grouping: string (must be in the dataframe columns)
    :param column_searched_for_mode: string (must be in the dataframe columns)
    :param fill_na_with: Int (value with which to replace empty values)
    :param create_label_column: Boolean (create the label column on the returned dataFrame)
    :param create_count_column: Boolean (create the count column on the returned dataFrame)
    :param create_percent_column: Boolean (create the percent column on the returned dataFrame)

    :return:
    """
    import pandas as pd
    import sys

    assert isinstance(database, pd.DataFrame), "df is not a DataFrame, it is : %s"%(type(database))
    assert column_for_grouping in database.columns, "Group is not in DataFrame"
    assert column_searched_for_mode in database.columns, "Column is not in DataFrame"
    assert isinstance(fill_na_with, int)
    assert isinstance(create_label_column, bool)
    assert isinstance(create_count_column, bool)
    assert isinstance(create_percent_column, bool)

    database = database.fillna(fill_na_with)

    col_count   = database[column_searched_for_mode].groupby(database[column_for_grouping]).count()
    distinct_value = database[column_searched_for_mode].groupby(database[column_for_grouping]).agg(lambda x: len(x.value_counts().values))
    mode_value  = database[column_searched_for_mode].groupby(database[column_for_grouping]).agg(lambda x: x.value_counts().index [0])
    mode_count  = database[column_searched_for_mode].groupby(database[column_for_grouping]).agg(lambda x: x.value_counts().values[0])
    pct_mode    = mode_count/col_count

    mode_value.name = "mode_%s"%(column_searched_for_mode)
    mode_count.name = "cnt_mode_%s"%(column_searched_for_mode)
    pct_mode.name   = "pct_mode_%s"%(column_searched_for_mode)
    distinct_value.name = "distinct_val_for_%s"%(column_searched_for_mode)


    mode_value = convert_serie_to_df(mode_value, column_for_grouping)
    mode_count = convert_serie_to_df(mode_count, column_for_grouping )
    pct_mode = convert_serie_to_df(pct_mode, column_for_grouping)
    distinct_val = convert_serie_to_df(distinct_value, column_for_grouping)

    new_df = pd.DataFrame()
    if create_label_column: new_df = merge_df(mode_value, mode_count) # new_df[header_mode_value ] = mode_value
    if create_count_column: new_df = merge_df(new_df , pct_mode ) # new_df[header_mode_count]=mode_count
    if create_percent_column: new_df = merge_df(new_df , distinct_val )#new_df[header_pct_mode]=pct_mode

    return new_df

def test(array, wanted_value):
    """
    Create an array of one for each elem in array being equals to the wanted value.
    Called by group.agg
    :param array:  array where to search for the value.
    :param wanted_value: value searched within the array.
    :return: float len(original array)
    """

    if len(array)==0:
        return 0
    nb_val = len(array)
    oks = [1 for x in array if x==wanted_value]
    nb_ok = len(oks)
    return nb_ok/nb_val

def get_percentage_of_a_value_in_a_col_by_group(database,col_to_group_by, colonne_to_test, searched_value, fill_na_with=0):
    """
    Create a new DataFrame containing two cols :
    (1) A col with all the modalities in col_to_gp_by
    (2) the pourcentage of [searched_value] for the [colonne_to_test] for each group

    :param database: pd.DataFrame
    :param col_to_group_by: string
    :param colonne_to_test: string
    :param searched_value: object
    :param fill_na_with: object (generally int)
    :return: pd.DataFrame : (two_columns)
    """
    import pandas as pd
    assert isinstance(database, pd.DataFrame), "database is not a pd.DataFrame, is is : %s"%(type(database))
    assert col_to_group_by in database.columns, "%s not in the database columns (%s)"%(col_to_group_by, database.collumns)
    assert colonne_to_test in database.columns, "%s not in the database columns (%s)"%(colonne_to_test, database.collumns)

    database   = database.fillna(fill_na_with)
    gpd_col     = database[colonne_to_test].groupby(database[col_to_group_by])
    pct_by_gp = gpd_col.agg(test, wanted_value=searched_value)
    new_col_name = "pct_%s_in_%s"%(searched_value, colonne_to_test)
    pct_by_gp.name=new_col_name
    return convert_serie_to_df(pct_by_gp, col_to_group_by)

def deal_with_continuous_column(database, col_to_group_by, col_to_analyse, fill_na_with=0):
    """
    Calculate some aggregate over a column, trying to convert it from string to in (values after dot are lost).
    :param database:
    :param col_to_group_by:
    :param col_to_analyse:
    :param fill_na_with:
    :return:
    """
    import pandas as pd
    assert isinstance(database, pd.DataFrame), "database is not a panda dataframe, it is : %s"%(type(database))
    assert isinstance(col_to_group_by, str), "col_to_group_by is not a str, it is : %s"%(type(col_to_group_by))
    assert isinstance(col_to_analyse, str), "col_to_analyse is not a str, it is : %s"%(type(col_to_analyse))
    assert isinstance(fill_na_with, int), "fill_na_with is not a int, it is : %s"%(type(fill_na_with))
    assert col_to_group_by in database.columns,"col_to_group_by (%s) is not in database's cols :[%s] "%(col_to_group_by , database.columns)
    assert col_to_analyse in database.columns,"col_to_analyse (%s) is not in database's cols :[%s] "%(col_to_analyse , database.columns)


    print "in"
    try:
        gp = database[col_to_analyse].groupby(database[col_to_group_by]).mean()
        gp = database[col_to_analyse].groupby(database[col_to_group_by])
    except Exception as e:
        try:
            # the data is not recognise as numeric
            # we try to convert it (from string)

            v0 = database[col_to_analyse].values
            v0 = [v.strip().replace(" ", "") for v in v0]
            try     : v1 = [int(v[:v.find(",")]) for v in v0]
            except  : v1 = [int(v[:v.find(".")]) for v in v0]

            i = database[col_to_analyse].index
            s = pd.Series(v1, index=i)
            gp = s.groupby(database[col_to_group_by])
        except Exception as e :
            print "deal_with_continuous_column : %s "%(e)


    gp_mean = gp.mean()
    gp_sum  = gp.sum()
    gp_max  = gp.max()
    gp_min  = gp.min()
    gp_std  = gp.std()


    sum_name   = "sum_of_%s"%(col_to_analyse)
    mean_name   = "mean_of_%s"%(col_to_analyse)
    max_name    =  "max_of_%s"%(col_to_analyse)
    min_name    =  "min_of_%s"%(col_to_analyse)
    std_name    =  "std_of_%s"%(col_to_analyse)

    gp_sum.name = sum_name
    gp_mean.name = mean_name
    gp_max.name  =  max_name
    gp_min.name  =  min_name
    gp_std.name  =  std_name

    df_sum = convert_serie_to_df(gp_sum, col_to_group_by)
    df_mean = convert_serie_to_df(gp_mean, col_to_group_by)
    df_max  = convert_serie_to_df(gp_max , col_to_group_by)
    df_min  = convert_serie_to_df(gp_min , col_to_group_by)
    df_std  = convert_serie_to_df(gp_std , col_to_group_by)

    df = merge_df(df_mean, df_std)
    df = merge_df(df, df_sum)
    df = merge_df(df, df_min)
    df = merge_df(df, df_max)

    return df


def get_delay_between_to_dates_by_group(database, col_to_group_by, col_date_1, col_date_2):
    """

    :param database:
    :param col_to_group_by:
    :param col_date_1:
    :param col_date_2:
    :return:
    """
    import pandas as pd

    name ="delay_%s_moins_%s"%(col_date_2, col_date_1)

    col_1 = pd.to_datetime(database[col_date_1])
    col_2  = pd.to_datetime(database[col_date_2])


    delay = pd.DataFrame()
    delay [col_to_group_by]=database[col_to_group_by]
    delay [name]=col_2 - col_1
    modes_delay = find_mod_group(delay , col_to_group_by, name)
    print "modes_delay.shape = ", modes_delay.shape
    return modes_delay


def get_percentage_of_a_value_in_a_col(dataframe, colonne, searched_value):
    serie=dataframe[colonne]
    mask = serie==searched_value
    nb_ok = mask.value_counts()[True]
    pct_ok = nb_ok / len(mask)
    return pct_ok




def clean_string(string):
    string.replace("é", "e")
    string.replace("è", "e")
    string.replace(" ", "_")

    a = [x.lower()  for x in string if x.lower() in "_azertyuiopqsdfghjklmwxcvbn1234567890".lower()]

    return ''.join(a)

def clean_string_array(array):

    return [ clean_string(x) for x in array ]


def enforce_float_for(x):
    if isinstance(x, float):
        return x
    try:
        return float(x)
    except:
        if isinstance(x, str):
            try:
                return float(x.replace(" ", "").replace(",", "."))
            except Exception as e:
                print e
                return None


def enforce_float(df, column):
    df[column].apply(enforce_float_for)


def select_columns_based_on_names(table):
    #
    # select the columns based on names
    #
    dates       = select_items_beginning_with(table.columns, "dt_"       )
    codes       = select_items_beginning_with(table.columns, "cd_"       )
    labels  = select_items_beginning_with(table.columns, "LB_"       )
    flags   = select_items_beginning_with(table.columns, "flag"      )
    flags2  = select_items_beginning_with(table.columns, "FG_"      )
    flags3  = select_items_beginning_with(table.columns, "EST_"      )
    ca      = select_items_beginning_with(table.columns, "CA_"       )
    alleg   = select_items_beginning_with(table.columns, "ALL"       )
    charge  = select_items_beginning_with(table.columns, "CC"        )
    cost    = select_items_beginning_with(table.columns, "COST_"     )
    cout    = select_items_beginning_with(table.columns, "COUT_"     )
    ct      = select_items_beginning_with(table.columns, "CT_"       )
    lib_    = select_items_beginning_with(table.columns, "LIB_"      )
    MB_         = select_items_beginning_with(table.columns, "MB_"       )
    MARGE       = select_items_beginning_with(table.columns, "MARGE_"    )
    salaire     = select_items_beginning_with(table.columns, "sal_"    )
    salaire2    = select_items_beginning_with(table.columns, "salaire"    )
    date2       =select_items_beginning_with(table.columns, "date"    )
    lib2        =select_items_beginning_with(table.columns, "libelle"    )
    nb          =select_items_beginning_with(table.columns, "nb_"    )
    nb2         =select_items_beginning_with(table.columns, "nb"    )
    provision   =select_items_beginning_with(table.columns, "prov_"    )
    remises     =select_items_beginning_with(table.columns, "remises_"    )

    lib_2    = select_items_beginning_with(table.columns, "libe"      )
    code_2   =select_items_beginning_with(table.columns, "code"      )
    #
    # GROUP the columns depending on their category :
    #
    modalities  = codes + labels + lib_ +lib2 + lib_2 + code_2
    binary      = flags + flags2 + flags3
    continuous  = ca + alleg + charge + cost + cout + ct + MB_ + MARGE + salaire + salaire2 + nb + provision + remises + nb2
    dates       = dates + date2

    return modalities, binary, continuous, dates


def auto_analyse_on_columns_names(file1, file2, col_union_f1, col_union_f2, col_gp_by, pickle_path, date_ref, binary_value_searched):
    import pandas as pd
    import sys
    import pickle
    import os
    #
    # Has the calculus already been saved/done ?
    #

    save_filename = "%s_&_%s_joined_by_%s_gpd_by_%s.pkl"%(get_file_name(file1), get_file_name(file2), ''.join(e if e in "azertyuiopqsdfghjklmwxcvbn" else "_" for e in col_union_f2 ), col_gp_by)
    save_in = os.path.join(pickle_path, save_filename)
    save_path = os.path.join(pickle_path, save_in)
    assert(path_is_not_a_file(save_path)), "Trying to save on an existing file (calculus already done ?): %s"%(save_path)
    print "going to save in %s"%(save_in)
    #
    #Do we have correct parameters to do the calculus ?
    #
    assert is_file(file2),"%s is not a path to a file"%(file2)

    table_1     =  get_dataframe(file1)
    table_2     =  get_dataframe(file2)
    table_1.columns = clean_string_array(table_1.columns)
    table_2.columns = clean_string_array(table_2.columns)
    print "table_1.columns = ",table_1.columns
    print "table_2.columns =", table_2.columns

    if(file1 != file2):
        database= pd.merge(table_1, table_2, left_on=col_union_f1, right_on=col_union_f2, how="left")
    else:
        database = table_1

    print database.shape
    assert(col_gp_by    in database.columns), "Declared grouping columns [%s] is not in the database's columns (listed below) :\n%s\n Pbm : Declared grouping columns [%s] is not in the database's columns (listed above)."%(col_gp_by, "\n".join(database.columns), col_gp_by)
    if date_ref : assert(date_ref     in database.columns or not date_ref ), "Declared date ref columns [%s] is not in the database's columns (listed below) :\n%s\n Pbm : Declared grouping columns [%s] is not in the database's columns (listed above)."%(date_ref, "\n".join(database.columns), date_ref)

    #
    # PREPARATION
    #

    database = database.fillna(0)
    dfs = []

    #
    # select the columns based on names
    #
    dates   = select_items_beginning_with(database.columns, "dt_"           )
    codes   = select_items_beginning_with(database.columns, "cd_"           )      
    labels  = select_items_beginning_with(database.columns, "LB_"           )
    flags   = select_items_beginning_with(database.columns, "flag"          )
    flags2   = select_items_beginning_with(database.columns, "FG_"          )
    flag3   = select_items_beginning_with(database.columns, "EST_"          )
    ca      = select_items_beginning_with(database.columns, "CA_"           )
    alleg   = select_items_beginning_with(database.columns, "ALL"           )
    charge  = select_items_beginning_with(database.columns, "CC"            )
    cost    = select_items_beginning_with(database.columns, "COST_"         )
    cout    = select_items_beginning_with(database.columns, "COUT_"         )
    ct      = select_items_beginning_with(database.columns, "CT_"           )
    lib_    = select_items_beginning_with(database.columns, "LIB_"          )
    MB_     = select_items_beginning_with(database.columns, "MB_"           )
    MARGE   = select_items_beginning_with(database.columns, "MARGE_"        )
    salaire = select_items_beginning_with(database.columns, "sal_"          )
    salaire2 = select_items_beginning_with(database.columns, "salaire"      )
    date2    =select_items_beginning_with(database.columns, "date"          )
    lib2     =select_items_beginning_with(database.columns, "libelle"       )
    nb       =select_items_beginning_with(database.columns, "nb_"           )
    #
    # GROUP the columns depending on their category :
    #
    modalities  = codes + labels + lib_ +lib2
    binary      = flags + flags2 + flag3
    continuous  = ca + alleg + charge + cost + cout + ct + MB_ + MARGE + salaire + salaire2 + nb
    dates       = dates + date2
    #
    # calculus on the number of column taken into account
    #
    a_traiter = modalities + binary + continuous + dates
    non_traitees = set(database.columns) - set(a_traiter)
    print "%s Non traitee : %s"%(len(non_traitees),non_traitees)

    #-------------------------------------------------------------
    #           deal with each type of col
    #-------------------------------------------------------------

    print "\nfor date columns :"
    for date in dates:
        print "Dealing with col : %s"%(date)
        if date !=date_ref:
            m = get_delay_between_to_dates_by_group(database, col_gp_by   , date_ref , date)
            assert isinstance(m, pd.DataFrame), "not a DataFrame : m is %s"%(type(m))
            dfs.append(m)

    print "\nfor binary columns:"
    for flag in binary:
        print "Dealing with col : %s"%(flag)
        m = get_percentage_of_a_value_in_a_col_by_group(database, col_gp_by, flag, binary_value_searched)
        assert isinstance(m, pd.DataFrame), "not a DataFrame : m is %s"%(type(m))
        dfs.append(m)

    print "\nfor modalities columns"
    for label in modalities:
        print "Dealing with col : %s"%(label)
        m = find_mod_group(database, col_gp_by   , label )
        assert isinstance(m, pd.DataFrame), "not a DataFrame : m is %s"%(type(m))
        dfs.append(m)

    print "\nfor continuous coloumns :"
    for colonne_continue in continuous:
        print "Dealing with col : %s"%(colonne_continue)
        m = deal_with_continuous_column(database, col_gp_by    , colonne_continue)

        assert isinstance(m, pd.DataFrame), "not a DataFrame : m is %s searching %s in %s (is in it ? %s ) "%(type(m), colonne_continue, database.columns, colonne_continue in database.columns)
        dfs.append(m)

    #---------------------------------------------------
    #   concatenate the dataframes
    #---------------------------------------------------

    merged_df = merge_df_array(dfs)

    print merged_df.shape

    #---------------------------------------------------
    #   Save the big dataframe
    #---------------------------------------------------

    with open(save_path , 'wb') as output_file:
        pickle.dump(merged_df, output_file)
    print "Pickled a %s dataframe into %s."%(merged_df.shape, save_path)

def merge_df_array(array_of_dataframes):
    """

    :param array_of_dataframes:
    :return:
    """
    import pandas as pd

    assert all([True if isinstance(x, pd.DataFrame) else False for x in array_of_dataframes ])," a parameter is not a DF : %s "%([type(x) for x in array_of_dataframes])
    merged_df = array_of_dataframes[0]
    for dataframe in array_of_dataframes[1:]:
        merged_df  = merge_df(merged_df , dataframe)
    return merged_df

def get_merge(pickle_dir):
    import pickle
    import pandas as pd
    assert is_dir(pickle_dir)

    pickle_paths = get_filepaths(pickle_dir, ".pkl")
    dfs = []
    for pickle_path in pickle_paths:
        print pickle_path
        df = pickle.load(open(pickle_path, 'rb'))
        assert isinstance(df, pd.DataFrame)
        dfs.append(df)

    return merge_df_array(dfs)



def try_to_transform_string_to_float(string):
    try:
        return float(string)
    except:
        try:
            return float(string.replace(",", "."))
        except:
            return string

def get_dataframe(path, sep=";", colonne_de_maille=False, error_bad_lines=False):
    """
    Call the pd.read_csv on the given path.
    :param path: string (complete path to a csv file)
    :param sep: string (csv separator)
    :param error_bad_lines: Boolean
    :return: pd.DataFrame
    """
    import pandas as pd

    assert is_file(path),"%s is not a path to a file"%(path)
    print "Loading %s"%(path)

    df          = pd.read_csv(path, sep=sep,  error_bad_lines=error_bad_lines)
    df.columns  = map(lambda x: clean_string(x).upper(), df.columns)
    df          = df.applymap(try_to_transform_string_to_float )

    if colonne_de_maille:
        assert colonne_de_maille in df.columns, "%s not in DF columns (%s)."%(colonne_de_maille, df.columns)
        df.index = df[colonne_de_maille]
    print "Datframe loaded "
    #do_pickle(df, "df_with_%s_as_col_de_maille"%(colonne_de_maille))
    return df

def analysis_initialisation(path_to_the_main_table, colonne_de_maille, col_y, sep=";"):
    """
    Create a DF from the given path, group it by the given column,
    and create another DF indexed by the col value, and having a col with the groups generated by the groupby object.
    Replace [,] by [.] on all cells and try then to convert numeric values (calling convert_objects)

    :param path_to_the_main_table: string (path to a csv file)
    :param colonne_de_maille: string (column containing the values for mesh analysis)
    :param sep: string (cv separator)
    :param dtype: array (experimental : trying to path a dtype to the df :-s )
    :return: a groupby object and a DF (containing one column and indexed with the value of this column)
    """
    import pandas as pd
    import numpy as np
    """
        0) verify parameters
    """
    assert is_file(path_to_the_main_table), "%s is not a file"%(path_to_the_main_table)
    print "path_to_the_main_table = ", path_to_the_main_table
    """
        1) load Main table with the index being the "colonne de maille"
    """

    main_table = get_dataframe(path_to_the_main_table, sep, colonne_de_maille)
    main_table[colonne_de_maille] = main_table.index
    """
        2) Group the main table by the "colonne de maille" (which is now the index)
    """
    print "Grouping by index"
    grouped_o                       = main_table.groupby(main_table.index)
    """
        3) Extract Y
    """
    print "Extracting Y"
    y                   = pd.DataFrame()
    y[col_y]            = grouped_o[col_y].sum()
    y.index             = grouped_o.groups.keys()
    """
        4) Create aggregation DataFrame:
                index = colonne de maille
                une colonne avec la colonne de maille
                une colonne avec Y

    """
    print "Creating aggregation dataframe"
    aggregation                     = pd.DataFrame()
    aggregation[colonne_de_maille]  = grouped_o.groups.keys()
    aggregation.index               = grouped_o.groups.keys()
    aggregation["y"]                = y[col_y]
    aggregation[col_y]              = y[col_y]

    try:
        print "Initialisation finished, returning 3 df and a group : main = %s aggregation = %s y= %s"%(main_table.shape, aggregation.shape, y.shape)
    except:
        pass
    """
    try:
        #do_pickle(main_table, "main_df")
        #do_pickle(grouped_o, "grouped_o")
        #do_pickle(aggregation, "aggregation")
        #do_pickle(y, "y")
    except:
        print "Error in piclking"
    """

    return main_table, grouped_o, aggregation, y

def test (x):
    print len(x.value_counts)

def auto_analysis(big_dataframe, group_key, aggregation_df):
    import time
    import pandas as pd
    assert group_key in big_dataframe.columns, "%s not in DF columns (%s)"%(group_key, "\n".join(big_dataframe.columns))
    modalities, binaries, continuous, dates = select_columns_based_on_names(big_dataframe)

    gpd_df = big_dataframe.groupby(group_key)
    gpd_df.index = big_dataframe[group_key]
    start1 = title2("Auto Analysis")

    """ ============================
                modalities
        ============================"""
    for modality in modalities:
        print modality
        mode     = gpd_df[modality].agg([("mod_of_%s"%(modality)        ,lambda x: x.value_counts().index[0]                                if len(x.value_counts().index)>0 else False )])
        mode_pct = gpd_df[modality].agg([("pct_of_mod_of_%s"%(modality) ,lambda x: x.value_counts().values[0]/sum(x.value_counts().values)  if len(x.value_counts().index)>0 else False )])
        nb       = gpd_df[modality].agg([("nb_of_%s"%(modality)         ,lambda x:                                                             len(x.value_counts())                    )])

        aggregation_df = pd.merge(aggregation_df, mode,     left_index=True, right_index=True, how='left')
        aggregation_df = pd.merge(aggregation_df, mode_pct, left_index=True, right_index=True, how='left')
        aggregation_df = pd.merge(aggregation_df, nb,       left_index=True, right_index=True, how='left')

    """ ============================
                Binaries
        ============================"""
    for binary in binaries:
        print binary
        sum_binary      = gpd_df[binary].agg([("sum_of_%s"%(binary), sum)])
        aggregation_df  = pd.merge(aggregation_df, sum_binary, left_index=True, right_index=True, how='left')
    """ ============================
                continous
        ============================"""
    for continuum in continuous:
        print continuum
        try:
            aggregation_df["min_of_%s"%(continuum)]     = gpd_df[continuum].min()
            aggregation_df["median_of_%s"%(continuum)]  = gpd_df[continuum].median()
            aggregation_df["max_of_%s"%(continuum)]     = gpd_df[continuum].max()
        except pd.core.groupby.DataError as e:
            print "ATTENTION => %s is not numerical ! Trying to force conversion"%(continuum)
            try:
                big_dataframe[continuum] = big_dataframe[continuum].convert_objects(convert_numeric=True)
                gpd_df                   = big_dataframe.groupby(group_key)

                aggregation_df["min_of_%s"%(continuum)   ]  = gpd_df[continuum].min()
                aggregation_df["median_of_%s"%(continuum)]  = gpd_df[continuum].median()
                aggregation_df["max_of_%s"%(continuum)   ]  = gpd_df[continuum].max()
            except Exception as e :
                print e

    """ ============================
                End
        ============================"""
    auto_columns = modalities + binaries +  continuous + dates
    left_aside   = set(big_dataframe.columns) - set(auto_columns)
    return aggregation_df , left_aside

def count_specificities(input_df, gp_col, specific_cols, aggregation_df):
    """

    """
    import time
    import pandas as pd
    for x in specific_cols:
        assert x in input_df.columns, "col %s not in df's columns (%s) "%(x, input_df.columns)
    
    gpd_df = input_df.groupby(gp_col)

    start = time.time()
    title2("Specificity")
    for modality in specific_cols:
        print modality
        mode     = gpd_df[modality].agg([("mod_of_%s"%(modality)        ,lambda x: x.value_counts().index[0]                                if len(x.value_counts().index)>0 else False )])
        mode_pct = gpd_df[modality].agg([("pct_of_mod_of_%s"%(modality) ,lambda x: x.value_counts().values[0]/sum(x.value_counts().values)  if len(x.value_counts().index)>0 else False )])
        nb       = gpd_df[modality].agg([("nb_of_%s"%(modality)         ,lambda x:                                                             len(x.value_counts())                    )])

        aggregation_df = pd.merge(aggregation_df, mode,     left_index=True, right_index=True, how='left')
        aggregation_df = pd.merge(aggregation_df, mode_pct, left_index=True, right_index=True, how='left')
        aggregation_df = pd.merge(aggregation_df, nb,       left_index=True, right_index=True, how='left')




    delay = time.time()-start
    print "%s \tspecific in %.2f sec (%.2f / loop)"%(len(specific_cols), delay, delay/max(len(specific_cols),1))
    return aggregation_df


def automatic_df_treatment(main_df, specific, aggregation_df):

    modalities, binaries, continuous, dates = select_columns_based_on_names(main_df)
    auto = modalities + binaries+ continuous + dates


    left_aside = set(main_df.columns) - set(auto) - set(specific)


    for special in specific:
        aggregation[special] = gpd_df[special].count()


    for modality in modalities:
        aggregation["mod_of_%s"%(modality)]         = gpd_df[modality].agg(lambda x:x.value_counts().index[0])
        aggregation["prct_of_mod_of_%s"%(modality)] = gpd_df[modality].agg(lambda x:x.value_counts().values[0]/sum(x.value_counts().values))

    for binary in binaries:
        main_df[continuum]                  = main_df[continuum].convert_objects(convert_numeric=True)
        aggregation["pc_of_%s"%(binary)]    = gpd_df[binary].sum()

    for continuum in continuous:
        main_df[continuum] = main_df[continuum].convert_objects(convert_numeric=True)
        aggregation["min_of_%s"%(continuum)]    = gpd_df[continuum].min()
        aggregation["median_of_%s"%(continuum)] = gpd_df[continuum].median()
        aggregation["max_of_%s"%(continuum)]    = gpd_df[continuum].max()


def get_merge_from_file(left_filename, left_union_on, df_right, right_union_on, debug=False):
    """
    Create a DF from a path, and directly merge it with another (already created before) passed as parameter.
     Used to 'add' a 'reference column' to a file when creating a DF out of it.

    :param left_filename: string (path from which to create the new df)
    :param left_union_on: string (columns of the new df on which to make the merge)
    :param df_right: pandas.DataFrame (df from wich to extract the appended column)
    :param right_union_on: string (column on which to merge on the right dataframe)
    :param debug: boolean (print some info to screen)
    :return: pandas.DataFrame (created from the file path, and extended from the union with the right DF)
    """
    import pandas as pd
    import os
    """
        Getinng DF
    """

    df_left   = get_dataframe(left_filename, ";")
    assert left_union_on   in df_left.columns, "%s not in %s"%(left_union_on  , df_left.columns)
    """
        MERGING
    """
    unioned_df_left= pd.merge(df_left                   ,
                              df_right                  ,
                              left_on   = left_union_on ,
                              right_on  = right_union_on,
                              how       = 'left'        );
    """
        Verify
    """
    title2("Merged %s :"%(left_filename))
    if debug:
        print unioned_df_left.ix[unioned_df_left[analysis_level].notnull(), :]
    return unioned_df_left


def create_df_and_auto_aggregate(objet, filepath, collonne_de_maille, specific, aggregation, sep=";"):
    """
    Create a df from the givent filepath path, and call auto_analysis on the colonne de maille.
    Plus call count_specificites on the specific array. Both aggregating on the aggregation df.

    :param objet: string (Just to display on screen)
    :param filepath:  string (file path to the data for the csv)
    :param collonne_de_maille: string (column on which to apply the group for auto analysis)
    :param specific: array (columns where to apply count_specifities)
    :param aggregation: pandas.DataFrame (dataframe to complete with the aggregations)
    :return: pandas.DataFrame (completed aggregation passed as parameter)
    """
    """
        ALGORITHM
    """
    title (objet)

    df      = get_dataframe(filepath,sep, collonne_de_maille)

    aggregation, left_aside  = auto_analysis      (df, collonne_de_maille,           aggregation )
    aggregation             = count_specificities(df, collonne_de_maille, specific, aggregation )
    left_aside               = left_aside.difference(set(specific))

    """
        SUMMARY
    """

    print "%s : %s col left aside = [ %s ]"%(objet, len(left_aside), " ; ".join(list(left_aside)))
    print "aggregation shape = :  ", aggregation.shape
    title("%s - FIN"%(objet))
    del df
    return aggregation

def auto_aggregate_with_specificities(objet, input_dataframe, collonne_de_maille, specific, aggregation, sep=";"):
    """
    Create a df from the givent filepath path, and call auto_analysis on the colonne de maille.
    Plus call count_specificites on the specific array. Both aggregating on the aggregation df.

    :param objet: string (Just to display on screen)
    :param input_dataframe:  pandas.dataFrame (DataFrame from which to gruop and do auto analysis )
    :param collonne_de_maille: string (column on which to apply the group for auto analysis)
    :param specific: array (columns where to apply count_specifities)
    :param aggregation: pandas.DataFrame (dataframe to complete with the aggregations)
    :return: pandas.DataFrame (completed aggregation passed as parameter)
    """
    """
        ALGORITHM
    """
    title (objet)

    aggregation, left_aside  = auto_analysis      (input_dataframe, collonne_de_maille,           aggregation )
    aggregation              = count_specificities(input_dataframe, collonne_de_maille, specific, aggregation )
    left_aside               = left_aside.difference(set(specific))

    """
        SUMMARY
    """

    print "%s : %s col left aside = [ %s ]"%(objet, len(left_aside), " ; ".join(list(left_aside)))
    print "aggregation shape = :  ", aggregation.shape
    title("%s - FIN"%(objet))
    return aggregation

def test_date(x, format, erreurs, ):
    import datetime
    try:
        return datetime.datetime.strptime(x, format)
    except:
        for erreur in erreurs:
            if erreur in x:
                return None 
        raise

def enforce_date(df, date_colonne, date_format="", default_date = "01/01/2020", default_format="%d/%m/%Y", debug=False):
    """
        call datetime.strptime on the date_colonne of the given dataframe.
    """
    import pandas as pd
    import datetime
    assert isinstance(df, pd.DataFrame), "df is not a Dataframe, it is a [%s]"%(type(df))
    assert date_colonne in df.columns, "[%s] not in [%s]"%(date_colonne, df.columns)
    formats = [date_format, "%d-%M-%y", "%d-%M-%Y", "%d.%m.%y","%d-%m-%y", "%d-%m-%Y", "%d/%m/%y", "%d%b%Y:00:00:00", "%d-%m-%Y", 
                "%Y/%m/%d 00:00:00", "%Y-%m-%d 00:00:00"]
    erreurs = ["31DEC9999", "0986/09/14", "986-09-14 00:00:00"] 
    
    
    changed          = False
    for format_ in formats:        
        try:
            df[date_colonne]  = df[df[date_colonne].notnull()][date_colonne].apply(lambda x:  test_date(x, format_, erreurs))
            break
        except Exception as e:
            pass

    date_mini     = datetime.datetime.strptime("01-01-1900", "%d-%m-%Y")
    date_maxi     = datetime.datetime.strptime(default_date, default_format)
    
    print "nb de nan apres2 = ", df[date_colonne].isnull().sum()
    df[date_colonne] =  df[date_colonne].fillna(date_maxi)
    print "nb de nan apres3 = ", df[date_colonne].isnull().sum()
    
    df.loc[     df[df[date_colonne] < date_mini  ].index, date_colonne] = date_mini
    df.loc[     df[df[date_colonne] > date_maxi  ].index, date_colonne] = date_maxi

    if debug : print "impossible d'enforcer la colonne [%s] en date'"%date_colonne
    return False
        
def enforce_float_to(x, debug=False):
    """
        Try to transform an input (str or float) in float.
        For str inputs, delete blanks and change ',' by '.' before attempting conversion.

        :return: float or exception
    """

    to_return = ""
    if isinstance(x, int):
        return x
    if isinstance(x, float):
        return x

    try:
        return float(x)
    except Exception as e :
        if isinstance(x, str):
            try:
                return int(x.replace(" ", ""))
            except:
                try:
                                    
                    return float(x.replace(" ", "").replace(",", "."))
                except Exception as e:
                    r = []
                    for c in x:
                        if c in "1234567890.":
                            r.append(c)
                        else:
                            raise Exception("Found a car not in [1234567890.]")
                    r = ''.join(r)
                    try:return int(r)
                    except : return float(r)
        else:
            if debug : print "Impossible to enforce [%s] (type=%s)en float.Error = [%s]"%(x,type(x),  e)
            raise Exception

    return to_return 


def enforce_float(df, column, debug=False):
    """
    Call unary function 'enforce_float' over a DataFrame.
    """
    try:
        df[column].apply(lambda x : enforce_float_to(x))
        if debug : print "%s transformed in float"%column
    except Exception as e:
        if debug : print "impossible de transformer %s transformed in float"%column
        print e

def plot_column(df, col_name, save_path=False):
    import matplotlib.pyplot as plt
    h_size  = 2.5
    w_size  = 3.5
    n_row   = 1
    n_col   = 3
    axe_nb  = 0
    color1  = 'pink'
    color2  ='orange'
    print col_name
    fig     = plt.figure( figsize=(w_size*n_col,h_size*n_row))
    fig.subplots_adjust(hspace=0.4, wspace=0.6)
    # distribution
    axe_nb +=1
    ax1 = fig.add_subplot(n_row,n_col,axe_nb)
    ax1.set_xlabel('Satisfaction (10 = best)')
    try:
        df[col_name].plot(kind='hist', color='pink', title="%s distribution"%col_name)
    except:
        print 'pbm with df[col_name].plot(kind=hist, color=pink, title= s distribution col_name) : col_name = %s'%(col_name)
    #
    axe_nb +=1
    ax2 = fig.add_subplot(n_row,n_col,axe_nb)
    ax2.set_xlabel('Satisfaction (10 = best)')
    ax1.set_ylabel("Nb of responses")
    ax2.set_ylabel("Nb of responses")
    df[col_name].plot(kind='box', color='pink', title="%s distribution"%col_name)
    #
    axe_nb +=1
    ax3 = fig.add_subplot(n_row,n_col,axe_nb)
    y_max = df.groupby(lambda x: (x.year, x.month))[col_name].mean().max() +1
    y_min = df.groupby(lambda x: (x.year, x.month))[col_name].mean().min() -1
    ax3.set_ylim(y_min,y_max)
    ax3.plot(df.groupby(lambda x: (x.year, x.month))[col_name].mean(), color=color1)
    ax3.set_title("%s and Nb of answers"%col_name)
    ax3.set_ylabel("Mensual %s Mean (%s)"%(col_name, color1))
    ax3.set_xlabel("Month")
    ax4 = ax3.twinx()
    ax4.plot(df.groupby(lambda x: (x.year, x.month))[col_name].count(),  color=color2)
    ax4.set_ylabel("Mensual Nb of answers (%s)"%(color2))

    if save_path:
        fig.savefig(save_path)

    """
    ax5 = fig.add_subplot(2,2,4)
    ax5.hist(date_speedy.groupby(lambda x: (x.year, x.month))["Q7"].count(), color='pink')
    ax5.set_title("Q7 and Nb of answers")
    ax5.set_ylabel("Mensual Q7 Mean (pink)")
    """

def columns_examples(df, random=True, n_sample=3):
    """
    Retourne une matrice avec une analyse des colonnes : nom, type, et examples
    Parameters:
        df : Dataframe to be analysed  
            pd.Dataframee
        random : should we take random rows (using df.sample)
            boolean
        n_samples : nb of example to give
            int
    Return:
        pandas Dataframe
    """
    from collections import OrderedDict
    import pandas as pd
    test     = df[:n_sample].copy()
    if random :
        test = df.sample(n_sample).copy()
    types    = test.dtypes
    to_print = []
    for i, col in enumerate(test.columns):
        p          = OrderedDict()
        p ["col" ] = col  
        p ["type"] = types[i]
        for i, v in enumerate(test[col].values):
            p["examp_%s"%i] = str(v) 
        
        to_print.append(p)

    return pd.DataFrame(to_print)
def calculate_nunique(df):
    """
    Apply nunique() on each column of the dataframe
    Parameters:
        df: dataframe to be analysed
            pandas dataframe
    Return:
        Panda dataframe
            
    """
    import pandas as pd
    r = {col : df[col].nunique() for col in df.columns}
    return pd.DataFrame(r,index=["nunique"]).T    
def add_quantile(df, nom_col):
    """
    cree une colonne quantilisee dans la df de la colonne passee en param
    """
    # Param
    col_quantile     = df[nom_col]
    new_col          = "quantile_{0}".format(nom_col)
    bins             = [0,0.05, 0.25, 0.5, 0.75, 0.95, 1]
    # algo
    quantiles        = col_quantile.quantile(bins)
    df[new_col]      = pd.cut(col_quantile, quantiles)
    return df