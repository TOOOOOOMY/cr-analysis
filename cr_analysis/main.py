"""
==========
Author: Tomoki WATANABE
Update: 10/06/2020
Version: 2.0.1
License: BSD License
Programing Language: Python3
==========
"""
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

settings = {
    "x_axis_title" : "Time [h]",
    "y_axis_title" : "Bioluminescence",
    "column_number" : 2,
    "y_axis_share_switch" : 1,
    "over_view_image_length" : 4.5,
    "over_view_image_width" : 5.0,
    "all_plot_column_number" : 12,
    "all_plot_image_length" : 2.5,
    "all_plot_image_width" : 2.5
}


settings_2 = {
    0 : ["black", "Group0"],
    1 : ["red", "Group1"],
    2 : ["orange", "Group2"],
    3 : ["green", "Group3"],
    4 : ["lightgreen", "Group4"],
    5 : ["blue", "Group5"],
    6 : ["lightblue", "Group6"],
    7 : ["yellow", "Group7"],
    8 : ["teal", "Group8"],
    9 : ["cyan", "Group9"],
    10 : ["gray", "Group10"],
}

def visualizer(file_name, # include .csv -> sample.csv
               file_path = "", # /content/sample.csv -> /content/
               graph_settings = settings,
               subtitle_and_color = settings_2,
               file_from = 1,
               sampling_period = 60,
               estimated_period = 24,
               over_view_plot_switch = 1,
                all_plot_switch = 1
):
    ##x軸単位（「"」に囲まれた部分を書き換え、以下同じ）
    x_axis_title = graph_settings["x_axis_title"]
    ##y軸単位
    y_axis_title = graph_settings["y_axis_title"]

    ##Overview plotでのグラフ横列表示数（１～５、標準３）
    column_number = graph_settings["column_number"]

    ##All plotでのグラフ間Y軸共有の有無（共有無→０、有→１）
    y_axis_share_switch = graph_settings["y_axis_share_switch"]

    ##グループ番号毎の色（参考：https://matplotlib.org/examples/color/named_colors.html）、先頭から数字の０に対応

    ##Overview plot
    ###画像1枚あたりの縦サイズ
    ov_length = graph_settings["over_view_image_length"]
    ###画像1枚あたりの横サイズ
    ov_width = graph_settings["over_view_image_width"]

    ##All plot
    ###出力時の列数
    a_column = graph_settings["all_plot_column_number"]
    ###画像1枚あたりの縦サイズ
    a_length = graph_settings["all_plot_image_length"]
    ###画像1枚あたりの横サイズ
    a_width = graph_settings["all_plot_image_width"]


    def color_changer(data_number):
        COLOR = subtitle_and_color[int(data_number)][0] # color_list[int(data_number)]
        Subtitle = subtitle_and_color[int(data_number)][1] # subtitle_list[int(data_number)]
        return COLOR, Subtitle


    def well_namer(i):
        if  i <= 12:
            ROW = 'A'
            COLUMN = i
        elif i <= 24 :
            ROW = 'B'
            COLUMN = i-12
        elif i <=36 :
            ROW = 'C'
            COLUMN = i-24
        elif  i <= 48:
            ROW = 'D'
            COLUMN = i-36
        elif i <= 60 :
            ROW = 'E'
            COLUMN = i-48
        elif i <=72 :
            ROW = 'F'
            COLUMN = i-60
        elif  i <= 84:
            ROW = 'G'
            COLUMN = i-72
        else :
            ROW = 'H'
            COLUMN = i-84

        if COLUMN <= 9:
            Col = '0{}'.format(COLUMN)
        else :
            Col = COLUMN

        return ROW, Col


    def router(file_path, file_name, column_number):
        if file_name[-4:] != ".csv":
            print("ERROR ->\nPlease use csv file.")
            sys.exit()
        row_data = pd.read_csv("{0}{1}".format(file_path, file_name), engine="python", encoding="utf-8_sig")
        try:
            new_data = row_data.drop('Unnamed: 0', axis=1).T
            X_axis = round(row_data["Unnamed: 0"].iloc[1:].reset_index(drop=True).astype(float), 4)
        except KeyError:
            new_data = row_data.drop('Time', axis=1).T
            X_axis = round(row_data['Time'].iloc[1:].reset_index(drop=True).astype(float), 4)
        finally:
            try:
                all_data = new_data.drop(0, axis=1).T.reset_index(drop=True)
                data_name = file_name
            except:
                print("<==========\nCSV file Error. \n\nA1 cell needs to be 'Time' or blank.\n==========>")
                sys.exit()
            else:
                if y_axis_share_switch == 0:
                    Yaxis = "Not shared"
                else :
                    Yaxis = "Y shared"

                if over_view_plot_switch == 1:
                    colored_overview_n_columns(X_axis, new_data, all_data, data_name, Yaxis, column_number, x_axis_title, y_axis_title)
                else:
                    pass

                if all_plot_switch == 1:
                    all_plot(X_axis, new_data, all_data, data_name, Yaxis)
                else:
                    pass


    def colored_overview_n_columns(X_axis, new_data, all_data, data_name, Yaxis, n, x_axis_title, y_axis_title):
        group_list = sorted(list(set(new_data[0])))

        F_max = np.amax(np.amax(all_data))
        Y_max = -(-F_max//1000)*1000

        fig = plt.figure(figsize=(n*ov_width, -(-(len(group_list)+n)//n)*ov_length))
        for I in range (0, len(group_list)+1, 1):
            if n <= 1:
                ax =  fig.add_subplot(-(-(len(group_list)+n)//n), n, I+1)
            else :
                if I < 1:
                    ax =  fig.add_subplot(-(-(len(group_list)+n)//n), n, I+1)
                else:
                    ax =  fig.add_subplot(-(-(len(group_list)+n)//n), n, I + n)

            if I == 0:
                process_data = all_data
                name = 'ALL'
                color_number = "-"
                plot_line_list = []
                for i in range(0, len(group_list)):
                    plot_line = ax.plot(X_axis, new_data[new_data[0]==group_list[i]].drop(0, axis=1).T.reset_index(drop=True), color='{}'.format(subtitle_and_color[round(group_list[i])][0]), label=subtitle_and_color[round(group_list[i])][1])
                    plot_line_list.append(plot_line[0])
                ax.legend(plot_line_list, plot_line_list)
            else :
                process_data = new_data[new_data[0]==group_list[I-1]].drop(0, axis=1).T.reset_index(drop=True)
                name = subtitle_and_color[round(group_list[I-1])][1]
                color_number = "No.{}".format(round(group_list[I-1]))
                ax.plot(X_axis, process_data, color='{}'.format(subtitle_and_color[round(group_list[I-1])][0])) # color_list[round(group_list[I-1])]))
            #変数セット
            data_time_lenght = len(process_data)
            n_rythm = int(-(-(data_time_lenght/(60/sampling_period))//24))
            X_max = int(n_rythm*24)
            original_lenght = len(all_data.T)
            data_lenght = len(process_data.T)
            data_percentage = round(data_lenght/original_lenght*100, 1)

            each_title = '{0} - {1} ({2}), {3}well ({4}%)'.format(data_name, name, color_number, data_lenght, data_percentage)
            ax.set_title(each_title)
            ax.set_xticks(np.linspace(0, X_max, n_rythm+1))
            ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True)
            ax.set_xlabel(x_axis_title)
            if Yaxis == "Y shared":
                ax.set_ylim(0, Y_max)
            ax.set_ylabel(y_axis_title)
            ax.grid(axis="both")

        fig.tight_layout()
        plt.savefig( "{0} - overview_{1}_col_plot.jpg".format(data_name, n))
        plt.show()


    def all_plot(X_axis, new_data, all_data, data_name, Yaxis):
        F_max = np.amax(np.amax(new_data))
        Y_max = -(-F_max//1000)*1000
        fig = plt.figure(figsize=(a_column*a_width, -(-new_data.shape[0]//a_column)*a_length))
        print("file_from : {}".format(file_from))
        for i in range(1, new_data.shape[0]+1):
            ax =  fig.add_subplot(-(-new_data.shape[0]//a_column),a_column,i)

            if file_from == 0:
                ROW, Col = well_namer(i)
                Name = '{0}{1}'.format(ROW, Col)
            else :
                Name = new_data.index[i-1]

            try:
                show = new_data.T[Name]
            except KeyError:
                ax.set_title("No Data")
                continue

            try:
                COLOR, Subtitle = color_changer(show[0])
            except:
                ax.set_title("No Data")
                continue

            #変数セット
            Shaped_data = show.drop(0, axis=0).reset_index(drop=True)
            data_time_lenght = len(Shaped_data)
            n_rythm = int(-(-(data_time_lenght/(60/sampling_period))//24))
            X_max = int(n_rythm*24)

            ax.plot(X_axis, Shaped_data, color='{}'.format(COLOR))
            ax.set_title('{0} ({1})'.format(Name, Subtitle))
            ax.set_xticks(np.linspace(0, X_max, n_rythm+1))
            ax.set_xticks(np.linspace(0, X_max, n_rythm*4+1), minor=True)

            if Yaxis == "Y shared":
                function = ax.set_ylim(0, Y_max)
                Title = data_name + '-96well Plot (Y axis shared)'
            else :
                function = "#"
                Title = data_name + '-96well Plot (Y axis NOT shared)'
            function
            ax.grid(axis="both")

        fig.tight_layout()
        fig.suptitle(Title, fontsize=25)
        plt.subplots_adjust(top=0.95, left=0.05, bottom=0.08)
        fig.text(0.5, 0.02, x_axis_title, ha='center', va='center', fontsize=15)
        fig.text(0.02, 0.5, y_axis_title, ha='center', va='center', rotation='vertical', fontsize=15)
        fig.align_labels()
        image_name = data_name
        plt.savefig( "{} - All_plot.jpg".format(data_name))
        plt.show()


    router(file_path, file_name, column_number)