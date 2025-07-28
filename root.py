import datetime
import glob
import os
import pprint
from pathlib import Path
import geopandas as gpd
import pandas as pd


class MbaE:
    """
    **Mba'e** in Guarani means **Thing**.

    .. important::

        **Mba'e is the origin**. The the very-basic almost-zero level object.
        Deeper than here is only the Python builtin ``object`` class.


    **Examples:**

    Here's how to use the ``MbaE`` class:

    Import ``MbaE``:

    .. code-block:: python

        # import the object
        from plans.src_root import MbaE

    ``MbaE`` instantiation

    .. code-block:: python

        # MbaE instantiation
        m = MbaE(name="Algo", alias="al")

    Retrieve metadata (not all attributes)

    .. code-block:: python

        # Retrieve metadata (not all attributes)
        d = m.get_metadata()
        print(d)

    Retrieve metadata in a `pandas.DataFrame`

    .. code-block:: python

        # Retrieve metadata in a `pandas.DataFrame`
        df = m.get_metadata_df()
        print(df.to_string(index=False))

    Set new values for metadata

    .. code-block:: python

        # Set new values for metadata
        d2 = {"Name": "Algo2", "Alias": "al2"}
        m.set(dict_setter=d2)

    Boot attributes from csv file:

    .. code-block:: python

        # Boot attributes from csv file:
        m.boot(bootfile="/content/metadata.csv")


    """

    def __init__(self, name="MyMbaE", alias=None):
        """Initialize the ``MbaE`` object.

        :param name: unique object name
        :type name: str

        :param alias: unique object alias.
            If None, it takes the first and last characters from ``name``
        :type alias: str

        """
        # ------------ pseudo-static ----------- #
        # test
        #
        self.object_name = self.__class__.__name__
        self.object_alias = "mbae"

        # name
        self.name = name

        # alias
        self.alias = alias

        # handle None alias
        if self.alias is None:
            self._create_alias()

        # fields
        self._set_fields()

        # ------------ set mutables ----------- #
        self.bootfile = None
        self.folder_bootfile = "./"  # start in the local place

        # ... continues in downstream objects ... #

    def __str__(self):
        """The ``MbaE`` string"""
        str_type = str(type(self))
        str_df_metadata = self.get_metadata_df().to_string(index=False)
        str_out = "[{} ({})]\n{} ({}):\t{}\n{}".format(
            self.name,
            self.alias,
            self.object_name,
            self.object_alias,
            str_type,
            str_df_metadata,
        )
        return str_out

    def _create_alias(self):
        """If ``alias`` is ``None``, it takes the first and last characters from ``name``"""
        if len(self.name) >= 2:
            self.alias = self.name[0] + self.name[len(self.name) - 1]
        else:
            self.alias = self.name[:]

    def _set_fields(self):
        """Set fields names"""

        # Attribute fields
        self.name_field = "Name"
        self.alias_field = "Alias"

        # Metadata fields
        self.mdata_attr_field = "Attribute"
        self.mdata_val_field = "Value"
        # ... continues in downstream objects ... #

    def get_metadata(self):
        """Get a dictionary with object metadata.

        .. note::

            Metadata does **not** necessarily inclue all object attributes.

        :return: dictionary with all metadata
        :rtype: dict
        """
        dict_meta = {
            self.name_field: self.name,
            self.alias_field: self.alias,
        }
        return dict_meta

    def get_metadata_df(self):
        """Get a :class:`pandas.DataFrame` created from the metadata dictionary

        :return: :class:`pandas.DataFrame` with ``Attribute`` and ``Value``
        :rtype: :class:`pandas.DataFrame`
        """
        dict_metadata = self.get_metadata()
        df_metadata = pd.DataFrame(
            {
                self.mdata_attr_field: [k for k in dict_metadata],
                self.mdata_val_field: [dict_metadata[k] for k in dict_metadata],
            }
        )
        return df_metadata

    def set(self, dict_setter):
        """Set selected attributes based on an incoming dictionary

        :param dict_setter: incoming dictionary with attribute values
        :type dict_setter: dict
        """
        # ---------- set basic attributes --------- #
        self.name = dict_setter[self.name_field]
        self.alias = dict_setter[self.alias_field]

        # ... continues in downstream objects ... #

    def boot(self, bootfile):
        """Boot fundamental attributes from a ``csv`` table.

        :param bootfile: file path to ``csv`` table with metadata information.
            Expected format:

            .. code-block:: text

                Attribute;Value
                Name;ResTia
                Alias;Ra

        :type bootfile: str

        :return:
        :rtype: str
        """
        # ---------- update file attributes ---------- #
        self.bootfile = bootfile[:]
        self.folder_bootfile = os.path.dirname(bootfile)

        # get expected fields
        list_columns = [self.mdata_attr_field, self.mdata_val_field]

        # read info table from ``csv`` file. metadata keys are the expected fields
        df_info_table = pd.read_csv(bootfile, sep=";", usecols=list_columns)

        # setter loop
        dict_setter = {}
        for i in range(len(df_info_table)):
            # build setter from row
            dict_setter[df_info_table[self.mdata_attr_field].values[i]] = df_info_table[
                self.mdata_val_field
            ].values[i]

        # pass setter to set() method
        self.set(dict_setter=dict_setter)

        return None


class DataSet(MbaE):
    """
    The core ``DataSet`` base/demo object.
    Expected to hold one :class:`pandas.DataFrame`.
    This is a Base and Dummy object. Expected to be implemented downstream for
    custom applications.

    **Examples**

    Here's how to use the ``DataSet`` class:

    Import Dataset

    .. code-block:: python

        # import Dataset
        from plans.src_root import DataSet

    Instantiate DataSet Object

    .. code-block:: python

        # instantiate DataSet object
        ds = DataSet(name="DataSet_1", alias="DS1")

    Set Object and Load Data

    .. code-block:: python

        # set object and load data.
        # Note: this dummy object expects "RM", "P", and "TempDB" as columns in data
        ds.set(
            dict_setter={
                "Name": "DataSet_2",
                "Alias": "DS2",
                "Color": "red",
                "Source": "",
                "Description": "This is DataSet Object",
                "File_Data": "/content/data_ds1.csv"
            },
            load_data=True
        )

    Check Data

    .. code-block:: python

        # check data `pandas.DataFrame`
        print(ds.data.head())

    Reload New Data from File

    .. code-block:: python

        # re-load new data from file
        ds.load_data(file_data="/content/data_ds2.csv")

    Get Basic Visual

    .. code-block:: python

        # get basic visual
        ds.view(show=True)

    Customize View Parameters

    .. code-block:: python

        # customize view parameters via the view_specs attribute:
        ds.view_specs["title"] = "My Custom Title"
        ds.view_specs["xlabel"] = "The X variable"
        ds.view(show=True)

    Save the Figure

    .. code-block:: python

        # save the figure
        ds.view_specs["folder"] = "path/to/folder"
        ds.view_specs["filename"] = "my_visual"
        ds.view_specs["fig_format"] = "png"
        ds.view(show=False)


    """

    def __init__(self, name="MyDataSet", alias="DS0"):
        """Initialize the ``DataSet`` object.
        Expected to increment superior methods.

        :param name: unique object name
        :type name: str

        :param alias: unique object alias.
            If None, it takes the first and last characters from name
        :type alias: str

        """
        # ------------ call super ----------- #
        super().__init__(name=name, alias=alias)
        # overwriters
        self.object_alias = "DS"

        # ------------ set mutables ----------- #
        self.file_data = None
        self.folder_data = None
        self.data = None
        self.size = None

        # descriptors
        self.source_data = None
        self.descri_data = None

        # ------------ set defaults ----------- #
        self.color = "blue"
        self.file_data_sep = ";"

        # UPDATE
        self.update()

        # ... continues in downstream objects ... #

    def __str__(self):
        """
        The ``DataSet`` string.
        Expected to overwrite superior methods.

        """
        str_super = super().__str__()
        if self.data is None:
            str_df_data = "None"
            str_out = "{}\nData:\n{}\n".format(str_super, str_df_data)
        else:
            # first 5 rows
            str_df_data_head = self.data.head().to_string(index=False)
            str_df_data_tail = self.data.tail().to_string(index=False)
            str_out = "{}\nData:\n{}\n ... \n{}\n".format(
                str_super, str_df_data_head, str_df_data_tail
            )
        return str_out

    def _set_fields(self):
        """Set fields names.
        Expected to increment superior methods.

        """
        # ------------ call super ----------- #
        super()._set_fields()
        # Attribute fields
        self.filedata_field = "File_Data"
        self.size_field = "Size"
        self.color_field = "Color"
        self.source_data_field = "Source"
        self.descri_data_field = "Description"

        # ... continues in downstream objects ... #

    def _set_view_specs(self):
        """Set view specifications.
        Expected to overwrite superior methods.

        :return: None
        :rtype: None
        """
        self.view_specs = {
            "folder": self.folder_data,
            "filename": self.name,
            "fig_format": "jpg",
            "dpi": 300,
            "title": self.name,
            "width": 5 * 1.618,
            "height": 5 * 1.618,
            "xvar": "RM",
            "yvar": "TempDB",
            "xlabel": "RM",
            "ylabel": "TempDB",
            "color": self.color,
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None,
        }
        return None

    def get_metadata(self):
        """Get a dictionary with object metadata.
        Expected to increment superior methods.

        .. note::

            Metadata does **not** necessarily inclue all object attributes.

        :return: dictionary with all metadata
        :rtype: dict
        """
        # ------------ call super ----------- #
        dict_meta = super().get_metadata()

        # customize local metadata:
        dict_meta_local = {
            self.size_field: self.size,
            self.color_field: self.color,
            self.source_data_field: self.source_data,
            self.descri_data_field: self.descri_data,
            self.filedata_field: self.file_data,
        }

        # update
        dict_meta.update(dict_meta_local)
        return dict_meta

    def update(self):
        """Refresh all mutable attributes based on data (includins paths).
        Base method. Expected to be incremented downstrem.

        :return: None
        :rtype: None
        """
        # refresh all mutable attributes

        # set fields
        self._set_fields()

        if self.data is not None:
            # data size (rows)
            self.size = len(self.data)

        # update data folder
        if self.file_data is not None:
            # set folder
            self.folder_data = os.path.abspath(os.path.dirname(self.file_data))
        else:
            self.folder_data = None

        # view specs at the end
        self._set_view_specs()

        # ... continues in downstream objects ... #
        return None

    def set(self, dict_setter, load_data=True):
        """Set selected attributes based on an incoming dictionary.
        Expected to increment superior methods.

        :param dict_setter: incoming dictionary with attribute values
        :type dict_setter: dict

        :param load_data: option for loading data from incoming file. Default is True.
        :type load_data: bool

        """
        super().set(dict_setter=dict_setter)

        # ---------- settable attributes --------- #

        # COLOR
        self.color = dict_setter[self.color_field]

        # DATA: FILE AND FOLDER
        # handle if only filename is provided
        if os.path.isfile(dict_setter[self.filedata_field]):
            file_data = dict_setter[self.filedata_field][:]
        else:
            # assumes file is in the same folder as the boot-file
            file_data = os.path.join(
                self.folder_bootfile, dict_setter[self.filedata_field][:]
            )
        self.file_data = os.path.abspath(file_data)

        # -------------- set data logic here -------------- #
        if load_data:
            self.load_data(file_data=self.file_data)

        # -------------- update other mutables -------------- #
        self.update()

        # ... continues in downstream objects ... #

    def load_data(self, file_data):
        """Load data from file. Expected to overwrite superior methods.

        :param file_data: file path to data.
        :type file_data: str
        :return: None
        :rtype: None
        """

        # -------------- overwrite relative path input -------------- #
        self.file_data = os.path.abspath(file_data)

        # -------------- implement loading logic -------------- #
        default_columns = {
            #'DateTime': 'datetime64[1s]',
            "P": float,
            "RM": float,
            "TempDB": float,
        }
        # -------------- call loading function -------------- #
        self.data = pd.read_csv(
            self.file_data,
            sep=self.file_data_sep,
            dtype=default_columns,
            usecols=list(default_columns.keys()),
        )

        # -------------- post-loading logic -------------- #
        self.data.dropna(inplace=True)

        # -------------- update other mutables -------------- #
        self.update()

        # ... continues in downstream objects ... #

        return None

    def view(self, show=True):
        """Get a basic visualization.
        Expected to overwrite superior methods.

        :param show: option for showing instead of saving.
        :type show: bool

        :return: None or file path to figure
        :rtype: None or str

        **Notes:**

        - Uses values in the ``view_specs()`` attribute for plotting

        **Examples:**

        Simple visualization:

        >>> ds.view(show=True)

        Customize view specs:

        >>> ds.view_specs["title"] = "My Custom Title"
        >>> ds.view_specs["xlabel"] = "The X variable"
        >>> ds.view(show=True)

        Save the figure:

        >>> ds.view_specs["folder"] = "path/to/folder"
        >>> ds.view_specs["filename"] = "my_visual"
        >>> ds.view_specs["fig_format"] = "png"
        >>> ds.view(show=False)

        """
        # get specs
        specs = self.view_specs.copy()

        # --------------------- figure setup --------------------- #
        fig = plt.figure(figsize=(specs["width"], specs["height"]))  # Width, Height

        # --------------------- plotting --------------------- #
        plt.scatter(
            self.data[specs["xvar"]],
            self.data[specs["yvar"]],
            marker=".",
            color=specs["color"],
        )

        # --------------------- post-plotting --------------------- #
        # set basic plotting stuff
        plt.title(specs["title"])
        plt.ylabel(specs["ylabel"])
        plt.xlabel(specs["xlabel"])

        # handle min max
        if specs["xmin"] is None:
            specs["xmin"] = self.data[specs["xvar"]].min()
        if specs["ymin"] is None:
            specs["ymin"] = self.data[specs["yvar"]].min()
        if specs["xmax"] is None:
            specs["xmax"] = self.data[specs["xvar"]].max()
        if specs["ymax"] is None:
            specs["ymax"] = self.data[specs["yvar"]].max()

        plt.xlim(specs["xmin"], specs["xmax"])
        plt.ylim(specs["ymin"], 1.2 * specs["ymax"])

        # Adjust layout to prevent cutoff
        plt.tight_layout()

        # --------------------- end --------------------- #
        # show or save
        if show:
            plt.show()
            return None
        else:
            file_path = "{}/{}.{}".format(
                specs["folder"], specs["filename"], specs["fig_format"]
            )
            plt.savefig(file_path, dpi=specs["dpi"])
            plt.close(fig)
            return file_path


class RecordTable(DataSet):
    """The core object for Record Tables. A Record is expected to keep adding stamped records
    in order to keep track of large inventories, catalogs, etc.
    All records are expected to have a unique Id. It is considered to be a relational table.


    Import RecordTable

    .. code-block:: python

        # Import RecordTable
        from plans.root import RecordTable

    Instantiate RecordTable Object

    .. code-block:: python

        # Instantiate RecordTable object
        rt = RecordTable(name="RecTable_1", alias="RT1")

    Setup custom columns for the data

    .. code-block:: python

        # Setup custom columns for the data
        rt.columns_data_main = ["Name", "Size"]  # main data
        rt.columns_data_extra = ["Type"]  # extra data
        rt.columns_data_files = ["File_P"]  # file-related
        rt.columns_data = rt.columns_data_main + rt.columns_data_extra + rt.columns_data_files

    Set Object Metadata and Load Data

    .. code-block:: python

        # Set object metadata and load data.
        # Note: this dummy object expects the following columns in data
        rt.set(
            dict_setter={
                "Name": "RecTable_01",
                "Alias": "RT01",
                "Color": "red",
                "Source": "-",
                "Description": "This is RecordTable Object",
                "File_Data": "/content/data_rt1.csv"
            },
            load_data=True
        )


    Check Data

    .. code-block:: python

        # Check data `pandas.DataFrame`
        print(rt.data.head())

    Load More Data from Other File

    .. code-block:: python

        # Load more new data from other file
        rt.load_data(file_data="/content/data_rt2.csv")

    Insert New Record

    .. code-block:: python

        # Insert new record from incoming dict
        d2 = {
            "Name": "k",
            "Size": 177,
            "Type": 'input',
            "File_P": "/filee.pdf",
        }
        rt.insert_record(dict_rec=d2)

    Edit Record

    .. code-block:: python

        # Edit record based on ``RecId`` and new dict
        d = {
            "Size": 34,
            "Name": "C"
        }
        rt.edit_record(rec_id="Rec0002", dict_rec=d)

    Archive a Record

    .. code-block:: python

        # Archive a record in the RT, that is ``RecStatus`` = ``Off``
        rt.archive_record(rec_id="Rec0003")

    Get a Record Dict by ID

    .. code-block:: python

        # Get a record dict by id
        d = rt.get_record(rec_id="Rec0001")
        print(d)

    Get a Record DataFrame by ID

    .. code-block:: python

        # Get a record `pandas.DataFrame` by id
        df = rt.get_record_df(rec_id="Rec0001")
        print(df.to_string(index=False))

    Load Record Data from CSV

    .. code-block:: python

        # Load record data from a ``csv`` file to a dict
        d = rt.load_record_data(file_record_data="/content/rec_rt2.csv")
        print(d)

    Export a Record to CSV

    .. code-block:: python

        # Export a record from the table to a ``csv`` file
        f = rt.export_record(
            rec_id="Rec0001",
            folder_export="/content",
            filename="export_rt2"
        )
        print(f)


    """

    def __init__(self, name="MyRecordTable", alias="RcT"):
        # prior attributes

        # ------------ call super ----------- #
        super().__init__(name=name, alias=alias)
        # overwriters
        self.object_alias = "RT"

        # --------- defaults --------- #
        self.id_size = 4  # for zfill
        self.layer_db = None

        # --------- customizations --------- #
        self._set_base_columns()
        self._set_data_columns()
        self._set_operator()

        # UPDATE
        self.update()

    def _set_fields(self):
        """Set fields names.
        Expected to increment superior methods.

        """
        # ------------ call super ----------- #
        super()._set_fields()
        # base columns fields
        self.recid_field = "RecId"
        self.rectable_field = "RecTable"
        self.rectimest_field = "RecTimestamp"
        self.recstatus_field = "RecStatus"
        # ... continues in downstream objects ... #

    def _set_base_columns(self):
        """Set base columns names.
        Base Method. Expected to be incremented in superior methods.

        """
        self.columns_base = [
            self.recid_field,
            self.rectable_field,
            self.rectimest_field,
            self.recstatus_field,
        ]
        # ... continues in downstream objects ... #

    def _set_data_columns(self):
        """Set specifics data columns names.
        Base Dummy Method. Expected to be incremented in superior methods.

        """
        # Main data columns
        self.columns_data_main = [
            "Kind",
            "Value",
        ]
        # Extra data columns
        self.columns_data_extra = [
            "Category",
        ]
        # File-related columns
        self.columns_data_files = ["File_NF", "File_Invoice"]

        # concat all lists
        self.columns_data = (
                self.columns_data_main + self.columns_data_extra + self.columns_data_files
        )
        # ... continues in downstream objects ... #

    def _set_operator(self):
        """Set the builtin operator for automatic column calculations.
        This is a Base and Dummy method. It is expected to be overwrited and implemented downstream.

        :return: None
        :rtype: None
        """

        # ------------- define sub routines here ------------- #

        def func_file_status():
            return FileSys.check_file_status(files=self.data["File"].values)

        def func_sum():
            return None

        def func_age():
            return RecordTable.running_time(
                start_datetimes=self.data["Date_Birth"], kind="human"
            )

        # ---------------- the operator ---------------- #
        self.operator = {
            "Sum": func_sum,
            "Age": func_age,
            "File_Status": func_file_status,
        }
        # remove here for downstream objects!
        self.operator = None
        return None

    def _get_organized_columns(self):
        """Return the organized columns (base + data columns)

        :return: organized columns (base + data columns)
        :rtype: list
        """
        return self.columns_base + self.columns_data

    @staticmethod
    def get_timestamp():
        """Return a string timestamp

        :return: full timestamp text %Y-%m-%d %H:%M:%S
        :rtype: str
        """
        # compute timestamp
        _now = datetime.datetime.now()
        return str(_now.strftime("%Y-%m-%d %H:%M:%S"))

    def _last_id_int(self):
        """Compute the last ID integer in the record data table.

        :return: last Id integer from the record data table.
        :rtype: int
        """
        if self.data is None:
            return 0
        else:
            df = self.data.sort_values(by=self.recid_field, ascending=True)
            return int(df[self.recid_field].values[-1].replace("Rec", ""))

    def _next_recid(self):
        """Get the next record id string based on the existing ids.

        :return: next record id
        :rtype: str
        """
        last_id_int = self._last_id_int()
        next_id = "Rec" + str(last_id_int + 1).zfill(self.id_size)
        return next_id

    def _filter_dict_rec(self, input_dict):
        """Filter input record dictionary based on the expected table data columns.

        :param input_dict: input record dictionary
        :type input_dict: dict
        :return: filtered record dictionary
        :rtype: dict
        """
        # ------ parse expected fields ------- #
        # filter expected columns
        dict_rec_filter = {}
        for k in self.columns_data:
            if k in input_dict:
                dict_rec_filter[k] = input_dict[k]
        return dict_rec_filter

    def update(self):
        super().update()

        # ... continues in downstream objects ... #
        return None

    def save(self):
        """
        Save the data to the sourced file data.

        .. danger::

            This method **overwrites** the sourced data file.


        :return: integer denoting succesfull save (0) or file not found (1)
        :rtype: int
        """
        if self.file_data is not None:
            # handle filename
            filename = os.path.basename(self.file_data).split(".")[0]
            # handle folder
            folder_export = os.path.dirname(self.file_data)
            # convert and overwrite layer
            gdf = gpd.GeoDataFrame(self.data)
            gdf.to_file(Path(f"{folder_export}/{filename}.gpkg"), layer=self.layer_db, driver="GPKG")
            return True
        else:
            return False

    def export(self, folder_export=None, filename=None, filter_archive=False):
        """Export the ``RecordTable`` data.

        :param folder_export: folder to export
        :type folder_export: str
        :param filename: file name (name alone, without file extension)
        :type filename: str
        :param filter_archive: option for exporting only records with ``RecStatus`` = ``On``
        :type filter_archive: bool
        :return: file path is export is successfull (1 otherwise)
        :rtype: str or int
        """
        if filename is None:
            filename = self.name
        # append extension
        filename = filename + ".csv"
        if self.data is not None:
            # handle folders
            if folder_export is not None:
                filepath = os.path.join(folder_export, filename)
            else:
                filepath = os.path.join(self.folder_data, filename)
            # handle archived records
            if filter_archive:
                df = self.data.query("RecStatus == 'On'")
            else:
                df = self.data.copy()
            # filter default columns:
            df = df[self._get_organized_columns()]
            df.to_csv(filepath, sep=self.file_data_sep, index=False, encoding="utf-8")
            return filepath
        else:
            return None

    def set(self, dict_setter, load_data=True):
        """Set selected attributes based on an incoming dictionary.
        Expected to increment superior methods.

        :param dict_setter: incoming dictionary with attribute values
        :type dict_setter: dict

        :param load_data: option for loading data from incoming file. Default is True.
        :type load_data: bool

        """
        # ignore color
        dict_setter[self.color_field] = None
        super().set(dict_setter=dict_setter, load_data=False)

        # ---------- set basic attributes --------- #

        # -------------- set data logic here -------------- #
        if load_data:
            self.load_data(file_data=self.file_data)
            self.refresh_data()

        # -------------- update other mutables -------------- #
        self.update()

        # ... continues in downstream objects ... #

    def refresh_data(self):
        """Refresh data method for the object operator.
        Performs spreadsheet-like formulas for columns.

        :return: None
        :rtype: None
        """
        if self.operator is not None:
            for c in self.operator:
                self.data[c] = self.operator[c]()
        # update object
        self.update()

    def load_data(self, file_data, layer):
        """Load data from geopackage file.
        Expected to overwrite superior methods.

        :param file_data: file path to geopackage.
        :type file_data: str
        :param layer: layer name in db.
        :type layer: str
        :return: None
        :rtype: None
        """
        # -------------- overwrite relative path input -------------- #
        self.file_data = os.path.abspath(file_data)
        self.layer_db = layer

        # -------------- implement loading logic -------------- #

        # -------------- call loading function -------------- #
        df = gpd.read_file(filename=self.file_data, layer=self.layer_db)

        # -------------- post-loading logic -------------- #
        self.set_data(input_df=df, append=True, inplace=True)

        return None

    def set_data(self, input_df, append=True, inplace=True):
        """Set RecordTable data from incoming dataframe.
        It handles if the dataframe has or not the required RT columns
        Base Method. Expected to be incremented downstream.

        :param input_df: incoming dataframe
        :type input_df: dataframe

        :param append: option for appending the dataframe to existing data. Default True
        :type append: bool

        :param inplace: option for overwrite data. Else return dataframe. Default True
        :type inplace: bool

        :return: None
        :rtype: None
        """
        list_input_cols = list(input_df.columns)

        # overwrite RecTable column
        input_df[self.rectable_field] = self.name

        # handle RecId
        if self.recid_field not in list_input_cols:
            # enforce Id based on index
            n_last_id = self._last_id_int()
            n_incr = n_last_id + 1
            input_df[self.recid_field] = [
                "Rec" + str(_ + n_incr).zfill(self.id_size) for _ in input_df.index
            ]
        else:
            # remove incoming duplicates
            input_df.drop_duplicates(subset=self.recid_field, inplace=True)

        # handle timestamp
        if self.rectimest_field not in list_input_cols:
            input_df[self.rectimest_field] = self.get_timestamp()

        # handle status
        if self.recstatus_field not in list_input_cols:
            input_df[self.recstatus_field] = "On"

        # Add missing columns with default values
        for column in self._get_organized_columns():
            if column not in input_df.columns:
                input_df[column] = ""
        df_merged = input_df[self._get_organized_columns()]

        # concatenate dataframes
        if append:
            if self.data is not None:
                df_merged = pd.concat([self.data, df_merged], ignore_index=True)

        if inplace:
            # pass copy
            self.data = df_merged.copy()
            return None
        else:
            return df_merged

    def insert_record(self, dict_rec):
        """
        Insert a record in the RT

        :param dict_rec: input record dictionary
        :type dict_rec: dict
        :return: None
        :rtype: None
        """

        # ------ parse expected fields ------- #
        # filter expected columns
        dict_rec_filter = self._filter_dict_rec(input_dict=dict_rec)
        # ------ set default fields ------- #
        # set table field
        dict_rec_filter[self.rectable_field] = self.name
        # create index
        dict_rec_filter[self.recid_field] = self._next_recid()
        # compute timestamp
        dict_rec_filter[self.rectimest_field] = self.get_timestamp()
        # set active
        dict_rec_filter[self.recstatus_field] = "On"

        # ------ merge ------- #
        # create single-row dataframe
        df = pd.DataFrame({k: [dict_rec_filter[k]] for k in dict_rec_filter})
        # concat to data
        self.data = pd.concat([self.data, df]).reset_index(drop=True)

        self.update()
        return None

    def edit_record(self, rec_id, dict_rec, filter_dict=True):
        """
        Edit RT record

        :param rec_id: record id
        :type rec_id: str
        :param dict_rec: incoming record dictionary
        :type dict_rec: dict
        :param filter_dict: option for filtering incoming record
        :type filter_dict: bool
        :return: None
        :rtype: None
        """
        # input dict rec data
        if filter_dict:
            dict_rec_filter = self._filter_dict_rec(input_dict=dict_rec)
        else:
            dict_rec_filter = dict_rec
        # include timestamp for edit operation
        dict_rec_filter[self.rectimest_field] = self.get_timestamp()

        # get data
        df = self.data.copy()
        # set index
        df = df.set_index(self.recid_field)
        # get filter series by rec id
        sr = df.loc[rec_id].copy()

        # update edits
        for k in dict_rec_filter:
            sr[k] = dict_rec_filter[k]

        # set in row
        df.loc[rec_id] = sr
        # restore index
        df.reset_index(inplace=True)
        self.data = df.copy()

        return None

    def archive_record(self, rec_id):
        """Archive a record in the RT, that is ``RecStatus`` = ``Off``

        :param rec_id: record id
        :type rec_id: str
        :return: None
        :rtype: None
        """
        dict_rec = {self.recstatus_field: "Off"}
        self.edit_record(rec_id=rec_id, dict_rec=dict_rec, filter_dict=False)
        return None

    def get_record(self, rec_id):
        """Get a record dict by id

        :param rec_id: record id
        :type rec_id: str
        :return: record dictionary
        :rtype: dict
        """
        # set index
        df = self.data.set_index(self.recid_field)

        # locate series by index and convert to dict
        dict_rec = {self.recid_field: rec_id}
        dict_rec.update(dict(df.loc[rec_id].copy()))
        return dict_rec

    def get_record_df(self, rec_id):
        """Get a record dataframe by id

        :param rec_id: record id
        :type rec_id: str
        :return: record dictionary
        :rtype: dict
        """
        # get dict
        dict_rec = self.get_record(rec_id=rec_id)
        # convert in vertical dataframe
        dict_df = {
            "Field": [k for k in dict_rec],
            "Value": [dict_rec[k] for k in dict_rec],
        }
        return pd.DataFrame(dict_df)

    def load_record_data(
        self, file_record_data, input_field="Field", input_value="Value"
    ):
        """Load record data from a ``csv`` file to a dict

        .. note::

            This method **does not insert** the record data to the ``RecordTable``.


        :param file_record_data: file path to ``csv`` file.
        :type file_record_data: str
        :param input_field: Name of ``Field`` column in the file.
        :type input_field:
        :param input_value: Name of ``Value`` column in the file.
        :type input_value:
        :return: record dictionary
        :rtype: dict
        """
        # load record from file
        df = pd.read_csv(
            file_record_data, sep=self.file_data_sep, usecols=[input_field, input_value]
        )
        # convert into a dict
        dict_rec_raw = {
            df[input_field].values[i]: df[input_value].values[i] for i in range(len(df))
        }

        # filter for expected data columns
        dict_rec = {}
        for c in self.columns_data:
            if c in dict_rec_raw:
                dict_rec[c] = dict_rec_raw[c]

        return dict_rec

    def export_record(self, rec_id, filename=None, folder_export=None):
        """Export a record from the table to a ``csv`` file.

        :param rec_id: record id
        :type rec_id: str
        :param filename: file name (name alone, without file extension)
        :type filename: str
        :param folder_export: folder to export
        :type folder_export: str
        :return: path to exported file
        :rtype: str
        """
        # retrieve dataframe
        df = self.get_record_df(rec_id=rec_id)
        # handle filename and folder
        if filename is None:
            filename = self.name + "_" + rec_id
        if folder_export is None:
            folder_export = self.folder_data
        filepath = os.path.join(folder_export, filename + ".csv")
        # save
        df.to_csv(filepath, sep=self.file_data_sep, index=False)
        return filepath

    def view(self, filter_status=True, recent=None):
        df = self.data.copy()
        df = df.query(f"{self.recstatus_field} == 'On'").copy().reset_index(drop=True)
        if recent is not None:
            df = df.sort_values(by="RecTimestamp", ascending=False)
            df = df.head(recent)
        df.drop(columns=self.columns_base, inplace=True)
        return df

    # ----------------- STATIC METHODS ----------------- #
    @staticmethod
    def timedelta_disagg(timedelta):
        """Util static method for dissaggregation of time delta

        :param timedelta: TimeDelta object from pandas
        :type timedelta: :class:`pandas.TimeDelta`
        :return: dictionary of time delta
        :rtype: dict
        """
        days = timedelta.days
        years, days = divmod(days, 365)
        months, days = divmod(days, 30)
        hours, remainder = divmod(timedelta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {
            "Years": years,
            "Months": months,
            "Days": days,
            "Hours": hours,
            "Minutes": minutes,
            "Seconds": seconds,
        }

    @staticmethod
    def timedelta_to_str(timedelta, dct_struct):
        """Util static method for string conversion of timedelta

        :param timedelta: TimeDelta object from pandas
        :type timedelta: :class:`pandas.TimeDelta`
        :param dct_struct: Dictionary of string strucuture. Ex: {'Expected days': 'Days'}
        :type dct_struct: dict
        :return: text of time delta
        :rtype: str
        """
        dct_td = RecordTable.timedelta_disagg(timedelta=timedelta)
        parts = []
        for k in dct_struct:
            parts.append("{}: {}".format(dct_struct[k], dct_td[k]))
        return ", ".join(parts)

    @staticmethod
    def running_time(start_datetimes, kind="raw"):
        """Util static method for computing the runnning time for a list of starting dates

        :param start_datetimes: List of starting dates
        :type start_datetimes: list
        :param kind: mode for output format ('raw', 'human' or 'age')
        :type kind: str
        :return: list of running time
        :rtype: list
        """
        # Convert 'start_datetimes' to datetime format
        start_datetimes = pd.to_datetime(start_datetimes)
        # Calculate the running time as a timedelta
        current_datetime = pd.to_datetime("now")
        running_time = current_datetime - start_datetimes
        # Apply the custom function to create a new column
        if kind == "raw":
            running_time = running_time.tolist()
        elif kind == "human":
            dct_str = {"Years": "yr", "Months": "mth"}
            running_time = running_time.apply(
                RecordTable.timedelta_to_str, args=(dct_str,)
            )
        elif kind == "age":
            running_time = [int(e.days / 365) for e in running_time]

        return running_time

class CompRT(RecordTable):

    def __init__(self):
        super().__init__(name="componentes", alias="CM")

    def _set_data_columns(self):
        # Main data columns
        self.columns_data_main = [
            "cod_componente","nm_componente","desc_componente"
        ]
        # Extra data columns
        self.columns_data_extra = []
        # File-related columns
        self.columns_data_files = []

        # concat all lists
        self.columns_data = self.columns_data_main[:]
        # ... continues in downstream objects ... #

class SubcRT(RecordTable):

    def __init__(self):
        super().__init__(name="subcomponentes", alias="SC")

    def _set_data_columns(self):
        # Main data columns
        self.columns_data_main = [
            "cod_subcomponente","desc_subcomponente","cod_componente"
        ]
        # Extra data columns
        self.columns_data_extra = []
        # File-related columns
        self.columns_data_files = []

        # concat all lists
        self.columns_data = self.columns_data_main[:]
        # ... continues in downstream objects ... #

class TematRT(RecordTable):

    def __init__(self):
        super().__init__(name="tematicas", alias="ES")

    def _set_data_columns(self):
        # Main data columns
        self.columns_data_main = [
            "cod_subcomponente", "nm_tematica"
        ]
        # Extra data columns
        self.columns_data_extra = []
        # File-related columns
        self.columns_data_files = []

        # concat all lists
        self.columns_data = self.columns_data_main[:]
        # ... continues in downstream objects ... #

class AcoesRT(RecordTable):

    def __init__(self):
        super().__init__(name="acoes", alias="AC")
        self._set_operator()

    def _set_data_columns(self):
        # Main data columns
        self.columns_data_main = [
            "cod_componente",
            "cod_subcomponente",
            "nm_tematica",
            "cod_acao",
            "desc_acao",
            "valor_investimento",
            "origem_investimento",
            "escala_acao"
        ]
        # Extra data columns
        self.columns_data_extra = []
        # File-related columns
        self.columns_data_files = []

        # concat all lists
        self.columns_data = self.columns_data_main[:]
        # ... continues in downstream objects ... #

    def _set_operator(self):
        """Set the builtin operator for automatic column calculations.

        :return: None
        :rtype: None
        """

        # ------------- define sub routines here ------------- #

        def update_acoes_codes():
            #
            ls_unique_sub = self.data["cod_subcomponente"].unique()
            ls_codes = []
            for sub_cod in ls_unique_sub:
                prefix = sub_cod.split(" ")[-1]
                df_q = self.data.query(f"cod_subcomponente == '{sub_cod}'").copy()
                ls_sub_codes = []
                c = 0
                for i in range(len(df_q)):
                    status_id = df_q[self.recstatus_field].values[i]
                    if status_id == "On":
                        c = c + 1
                        cod = f"acao {prefix}." + str(c)
                    else:
                        cod = "acao arquivada"
                    ls_sub_codes.append(cod)
                ls_codes = ls_codes + ls_sub_codes[:]

            return ls_codes


        # ---------------- the operator ---------------- #
        self.operator = {
            "cod_acao": update_acoes_codes,
        }

        return None

    def edit_record(self, cod_acao, dict_rec, filter_dict=True):
        if cod_acao not in set(self.data["cod_acao"]):
            print(f"Codigo {cod_acao} não encontrado!")
        else:
            # find action code
            df_q = self.data.query(f"cod_acao == '{cod_acao}'").copy()
            rec_id = df_q[self.recid_field].values[0]
            super().edit_record(rec_id, dict_rec, filter_dict)
            self.refresh_data()
        return None

    def insert_record(self, dict_rec):
        super().insert_record(dict_rec)
        self.refresh_data()
        return None

    def archive_record(self, cod_acao):
        if cod_acao not in set(self.data["cod_acao"]):
            print(f" >>> Código {cod_acao} não encontrado!")
            return False
        else:
            # find action code
            dict_rec = {self.recstatus_field: "Off"}
            self.edit_record(cod_acao=cod_acao, dict_rec=dict_rec, filter_dict=False)
            self.refresh_data()
            return True


    def insert(self, dc_acao):
        ls_cols = []
        ls_values = []
        for k in dc_acao:
            ls_cols.append(k)
            ls_values.append(dc_acao[k])
            if dc_acao[k] is None:
                print(f" >>> Campo vazio em '{k}'. Inserção cancelada.")
                return False
        _df = pd.DataFrame(
            {
                "Column": ls_cols,
                "Valor": ls_values
            }
        )
        print(f" >>> Inserir nova ação:\n")
        print(_df)
        print(" >>> Atenção: o arquivo será salvo com as mudanças")
        s = input(" >>> Confirmar inserção? (s/n) >> ").lower().strip()
        if s == "s":
            print(" >>> Inserção autorizada")
            self.insert_record(dict_rec=dc_acao)
            print(" >>> Inserção realizada\n")
            self.save()
        else:
            print(" >>> Inserção cancelada\n")
            return False
        return True


    def view_acao(self, cod_acao, dataframe=True):
            df_q = self.data.query(f"cod_acao == '{cod_acao}'").copy()
            ls_cols = [c for c in df_q.columns]
            ls_values = [df_q[c].values[0] for c in df_q.columns]

            if dataframe:
                output = {
                    "Coluna": ls_cols,
                    "Valor": ls_values
                }
                output = pd.DataFrame(output)
            else:
                output = {}
                for c in ls_cols:
                    output[c] = df_q[c].values[0]
            return output


    def edit(self, cod_acao, dc_acao):
        print(f"\n\n >>> Editar ação '{cod_acao}'")

        if cod_acao not in set(self.data["cod_acao"]):
            print(f" >>> Código '{cod_acao}' não encontrado!")
            print(" >>> Remoção cancelada")
            return False
        else:
            dc_acao_old = self.view_acao(cod_acao=cod_acao, dataframe=False)
            df_acao_new = pd.DataFrame(
                {"Coluna": [k for k in dc_acao],
                 "Valor atual": [dc_acao_old[k] for k in dc_acao],
                 "Valor novo": [dc_acao[k] for k in dc_acao]
                 }
            )
            print(f" >>> Ação '{cod_acao}' encontrada:\n")
            print(self.view_acao(cod_acao=cod_acao))
            print("\n >>> Novo atributos:")
            print(df_acao_new)
            print("\n")
            print(" >>> Atenção: o arquivo será salvo com as mudanças")
            s = input(" >>> Confirmar edição? (s/n) >> ").lower().strip()
            if s == "s":
                print(" >>> Edição autorizada")
                # find action code
                self.edit_record(cod_acao=cod_acao, dict_rec=dc_acao, filter_dict=False)
                self.refresh_data()
                print(" >>> Edição realizada\n")
                self.save()
                print(f" >>> Ação '{cod_acao}' atualizada:")
                print(self.view_acao(cod_acao=cod_acao))
                return True
            else:
                print(" >>> Edição cancelada\n")
                return False


    def remove(self, cod_acao):
        print(f"\n\n >>> Remover ação '{cod_acao}'")
        if cod_acao not in set(self.data["cod_acao"]):
            print(f" >>> Código '{cod_acao}' não encontrado!")
            print(" >>> Remoção cancelada")
            return False
        else:
            print(f" >>> Ação '{cod_acao}' encontrada:\n")
            print(self.view_acao(cod_acao=cod_acao))
            print("\n")
            print(" >>> Atenção: o arquivo será salvo com as mudanças")
            s = input(" >>> Confirmar remoção? (s/n) >> ").lower().strip()
            if s == "s":
                print(" >>> Remoção autorizada")
                # find action code
                dict_rec = {self.recstatus_field: "Off"}
                self.edit_record(cod_acao=cod_acao, dict_rec=dict_rec, filter_dict=False)
                self.refresh_data()
                print(" >>> Remoção realizada\n")
                self.save()
                return True
            else:
                print(" >>> Remoção cancelada\n")
                return False


class OrigemRT(RecordTable):

    def __init__(self):
        super().__init__(name="origem", alias="OR")

    def _set_data_columns(self):
        # Main data columns
        self.columns_data_main = [
            "origem_investimento", "categoria"
        ]
        # Extra data columns
        self.columns_data_extra = []
        # File-related columns
        self.columns_data_files = []

        # concat all lists
        self.columns_data = self.columns_data_main[:]
        # ... continues in downstream objects ... #

class EscalaRT(RecordTable):

    def __init__(self):
        super().__init__(name="escala", alias="ES")

    def _set_data_columns(self):
        # Main data columns
        self.columns_data_main = [
            "escala_acao", "categoria"
        ]
        # Extra data columns
        self.columns_data_extra = []
        # File-related columns
        self.columns_data_files = []

        # concat all lists
        self.columns_data = self.columns_data_main[:]
        # ... continues in downstream objects ... #

def get_tables():
    return {
        "componentes": CompRT(),
        "subcomponentes": SubcRT(),
        "tematicas": TematRT(),
        "acoes": AcoesRT(),
        "escala": EscalaRT(),
        "origem": OrigemRT(),
    }


def get_layer_names():
    return list(get_tables().keys())


def load_db(folder):
    print(">> carregando dados ...")
    # retrieve latest version
    ls_files = glob.glob(f"{folder}/pishne_db_*.gpkg")
    if len(ls_files) > 0:
        print("Ok. Arquivo encontrado na pasta.")
        ls_files.sort()
        file_db = Path(ls_files[-1])  # get the lastest
        # instantiate dictionary for holding tables
        dc_db = get_tables()
        # list layers
        ls_layers = get_layer_names()
        # loop over
        for layer in ls_layers:
            dc_db[layer].load_data(file_data=file_db, layer=layer)
        print("Dados carregados.")
        return dc_db
    else:
        print("Atenção! Arquivo do banco de dados não encontrado.")
        return None


def join_db(db):
    # obter dados
    gdf_acoes = db["acoes"].view(filter_status=True)
    gdf_subc = db["subcomponentes"].view(filter_status=True)
    gdf_comp = db["componentes"].view(filter_status=True)

    # unir acoes com subcomponentes
    df1 = pd.merge(left=gdf_acoes, right=gdf_subc, on="cod_subcomponente", how="left", suffixes=('', '_drop'))
    df1.drop([col for col in df1.columns if 'drop' in col], axis=1, inplace=True)

    # unir acoes com componentes
    df_uniao = pd.merge(left=df1, right=gdf_comp, on="cod_componente", how="left", suffixes=('', '_drop'))
    df_uniao.drop([col for col in df_uniao.columns if 'drop' in col], axis=1, inplace=True)

    # reorganizar ordem das colunas
    c1 = list(df_uniao.columns)
    c2 = c1[0:1] + c1[-2:] + c1[1:2] + c1[-3:-2] + c1[2:-3]
    df_uniao = df_uniao[c2]

    return df_uniao

def expand_db(db):
    df1 = join_db(db)
    '''
    print(df1.info())
    print(df1["valor_investimento"].sum())
    print("^^^^^^^^^^^^^^^^^^^^")
    '''
    ls_ufs = [
        "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"
    ]
    n_ufs = len(ls_ufs)
    df_escala = db["escala"].data
    ls_full = []
    for i in range(len(df_escala)):
        s_escala = df_escala["escala_acao"].values[i]
        s_cat = df_escala["categoria"].values[i]
        #print(s_escala)
        s_label = "Global"
        if s_cat == "UF" and s_escala in ls_ufs:
            filtered_df1 = df1[df1['escala_acao'].str.contains(s_escala, case=True)].copy()
            s_label = s_escala[:]
            filtered_df1["escala_local"] = s_label
        elif s_cat == "UF" and s_escala == "Todos Estados":
            filtered_df1 = df1[df1['escala_acao'].str.contains(s_escala, case=True, regex=False)].copy()
            ls_news = []
            for uf in ls_ufs:
                filtered_df2 = filtered_df1.copy()
                filtered_df2["escala_local"] = uf
                ls_news.append(filtered_df2.copy())
            filtered_df1 = pd.concat(ls_news).reset_index(drop=True)
        else:
            s_label == "all"
            filtered_df1 = df1[df1['escala_acao'].str.contains(s_escala, case=True, regex=False)].copy()
            filtered_df1["escala_local"] = s_escala
        #print(filtered_df1[["cod_acao", "valor_investimento", "escala_acao", "escala_local"]])
        #print("\n")
        ls_full.append(filtered_df1.copy())

    df_full = pd.concat(ls_full).reset_index(drop=True)
    df_full = df_full.sort_values(by="cod_acao").reset_index(drop=True)
    '''   
    print(df_full.info())
    print(df_full["valor_investimento"].sum())
    print("^^^^^^^^^^^^^^^^^^^^")
    print(df_full.head(20))
    '''
    return df_full

def summarize(db, subset):
    if subset == "escala_acao":
        subset = "escala_local"
    df = expand_db(db=db)
    #print(df[["escala_acao", "escala_local"]].sort_values(by="escala_local").head(20))
    # Aggregate stats of "value" field by "label" field
    df_ups = df.groupby(subset)['valor_investimento'].agg(['mean', 'sum', 'min', 'max', 'count']).reset_index()
    df_ups.rename(columns={
        "mean": "media",
        "sum": "soma",
        "count": "contagem",
    }, inplace=True)
    df_ups.sort_values(by="soma", inplace=True, ascending=False)
    df_ups.reset_index(drop=True, inplace=True)
    df_extra = pd.DataFrame(
        {
            subset: ["totais"],
            "media": df_ups["media"].mean(),
            "soma": df_ups["soma"].sum(),
            "min": df_ups["min"].min(),
            "max": df_ups["max"].max(),
            "contagem": df_ups["contagem"].sum(),
        }
    )
    df_ups = pd.concat([df_ups, df_extra])
    df_ups["unidade"] = "Mi R$"
    # enhance dataframe
    if subset == "cod_componente":
        df_ups = pd.merge(left=df_ups, right=db["componentes"].view(), on=subset, how="left")
    if subset == "cod_subcomponente":
        df_ups = pd.merge(left=df_ups, right=db["subcomponentes"].view(), on=subset, how="left")
    return df_ups



def gui_filter_value(db):
    from pishne.gui import slider_filter
    df = join_db(db=db)
    slider_filter(
        df=df,
        column="valor_investimento",
        label1="Ações filtradas",
        label2="Total R$ (Mi)"
    )


def gui_filter_category(df, col, contains, options):
    from pishne.gui import dropdown_filter
    dropdown_filter(
        df=df,
        column=col,
        label1="Ações filtradas",
        label2="Total R$ (Mi)",
        value_column="valor_investimento",
        contains=contains,
        options=options
    )

def gui_filter(db, field):
    dc = {
        "Temática": "nm_tematica",
        "Componente": "nm_componente",
        "Subcomponente":"cod_subcomponente",
        "Origem": "origem_investimento",
        "Escala": "escala_acao"
    }
    df = join_db(db=db)
    column = dc[field]
    b_contains = False
    ls_options = None
    if column == "escala_acao":
        b_contains = True
        ls_options = sorted(db["escala"].data["escala_acao"].unique())
    # call gui
    gui_filter_category(
        df=df,
        col=dc[field],
        contains=b_contains,
        options=ls_options
    )

def gui_form(db):
    from pishne.gui import action_form
    d = action_form(db=db, df=join_db(db))
    return d


def export_db2csv(db, use_gui=True, folder=None):
    jdf = join_db(db)
    if use_gui:
        from pishne.gui import download
        download(df=jdf, filename="pishne_data.csv")
    else:
        if folder is None:
            folder = "./"
        jdf.to_csv(f"{folder}/pishne_data.csv", sep=";", encoding="utf-8", index=False)


# deprecated
def __setup_db(folder):
    # retrieve latest version
    ls_files = glob.glob(f"{folder}/pishne_db_*.gpkg")
    ls_files.sort()
    file_db = Path(ls_files[-2]) # get the pre-last
    file_db2 = Path(ls_files[-1])  # get the last

    # instantiate dictionary for holding tables
    dc_db = get_tables()
    ls_layers = list(dc_db.keys())
    for layer in ls_layers:
        #layer = "acoes"
        df = gpd.read_file(filename=file_db, layer=layer)
        dc_db[layer].set_data(input_df=df, append=True, inplace=True)
        print(dc_db[layer].data.info())
        # export
        gdf = gpd.GeoDataFrame(data=dc_db[layer].data)
        # gdf must be a GeoDataFrame object
        gdf.to_file(file_db2, layer=layer, driver="GPKG")


    return 0

