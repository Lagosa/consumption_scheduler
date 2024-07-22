import EditRow from "@/components/EditRow.vue";
import UploadButton from "@/components/UploadButton.vue";
import axios from "axios";
import OperationsButton from "@/components/OperationsButton.vue";
import HeaderBand from "@/components/HeaderBand.vue";
import TableComponent from "@/components/TableComponent.vue";
import LineChart from "@/components/LineChart.vue";
import ChartContainer from "@/components/ChartContainer.vue";
import DownloadButton from "@/components/DownloadButton.vue";

export default {
    name: 'UploadPage',
    components: {
        DownloadButton,
        ChartContainer,
        LineChart, TableComponent, HeaderBand, OperationsButton: OperationsButton, UploadButton, EditRow},
    data() {
        return {
            device_description_file: null,
            comfort_file: null,
            initial_usage_file: null,
            configuration_file: null,
            target_curve_file: null,
            dataset_code_text: null,
            srcOneImg: require('@/assets/circle-1.png'),
            existingDatasetCodes: [],
            selected_dataset_code: "",
            availableOperationCodes: [],
            selected_operation_code: "",

            showLoading: false,
            showEmptyBackground: true,
            showTextResult: false,
            textResult: "",
            showTable: false,
            tables: [],

            showChart: false,
            charts:[],

            showDownload: false,
            showScheduleTable: false,
            tables_schedule: [],
        }
    },
    methods: {
        doScheduling() {
            let targetCurveFile = null
            if (this.target_curve_file != null) {
                targetCurveFile = this.target_curve_file[0]
            }

            let configurationFile = null
            if (this.configuration_file != null) {
                configurationFile = this.configuration_file[0]
            }

            let form = new FormData()
            form.append("dataset_code", this.selected_dataset_code)
            form.append("operation_code", this.selected_operation_code)
            form.append("target_curve", targetCurveFile)
            form.append("configuration", configurationFile)

            this.resetResultBlock()
            const url = "http://" + process.env.VUE_APP_SERVER_IP + ":" + process.env.VUE_APP_SERVER_PORT + "/scheduler/evaluate"
            this.startLoading()
            axios.post(url, form)
                .then(response => {
                    this.scrollToResult()
                    this.endLoading()
                    if (response.data.status != null) {
                        this.$store.dispatch("handleStatus", response.data.status)
                        if (response.data.status === "OPERATION_PERFORMED") {
                            this.handleOperationResult(response.data.result)
                        }
                    }
                })
                .catch(error => {
                    this.endLoading()
                    this.$store.dispatch("handleInternalError", error)
                })
        },
        doUpload() {
            const isUploadFieldValid = this.isUploadFieldsValid()
            if (!isUploadFieldValid) {
                return
            }

            const descriptionFile = this.device_description_file[0]
            const comfortFile = this.comfort_file[0]
            const usageFile = this.initial_usage_file[0]

            let form = new FormData()
            form.append("dataset_code", this.dataset_code_text)
            form.append("device_detail", descriptionFile)
            form.append("device_comfort", comfortFile)
            form.append("device_usage", usageFile)

            const url = "http://" + process.env.VUE_APP_SERVER_IP + ":" + process.env.VUE_APP_SERVER_PORT + "/scheduler/save_dataset"
            this.resetResultBlock()
            this.startLoading()
            axios.post(url, form)
                .then(response => {
                    this.endLoading()
                    this.showEmptyBackground = true

                    this.$store.dispatch("handleStatus", response.data.status)
                    if (response.data.status === "OK") {
                        this.existingDatasetCodes.unshift(this.dataset_code_text)

                        this.selected_dataset_code = this.dataset_code_text
                    }
                })
                .catch(error => {
                    this.endLoading()
                    this.showEmptyBackground = true
                    this.$store.dispatch("handleInternalError", error)
                })
        },
        handleOperationResult(results) {
            this.showEmptyBackground = false

            for (var result of results) {
                var data = result.data
                if (result.type === "TABLE") {
                    this.showTable = true
                    this.tables.push({
                        data: data.rows,
                        header: data.header,
                        title: data.title
                    })
                    continue
                }

                if (result.type === "CHART") {
                    this.showChart = true

                    this.charts.push({
                        title: data.title,
                        labels: data.label,
                        type: data.type,
                        datasets: data.valuesArray,
                        yAxisTitle: data.yAxisTitle,
                        xAxisTitle: data.xAxisTitle,
                    })
                    continue
                }

                if (result.type === "INFO") {
                    if (result.data === "FILE") {
                        this.makeRequestForFile()
                    }
                    continue
                }

                // if (result.type === "TABLE_SCHEDULE") {
                //     this.showScheduleTable = true
                //     this.tables_schedule.push({
                //         data: data.rows,
                //         header: data.header,
                //         title: data.title
                //     })
                //     continue
                // }

            }
        },
        makeRequestForFile() {
            const getFileURL = "http://" + process.env.VUE_APP_SERVER_IP + ":" + process.env.VUE_APP_SERVER_PORT + "/scheduler/solution_file"
            axios.get(getFileURL)
                .then(result => {
                    const url = window.URL.createObjectURL(new Blob([result.data]))
                    const linkElement = document.createElement("a")
                    linkElement.href = url
                    linkElement.id = "solution_link_element"
                    linkElement.setAttribute("download", "Schedule.csv")
                    document.body.appendChild(linkElement)
                    this.showDownload = true
                    this.showScheduleTable = true
                })
                .catch(error => {
                    this.showEmptyBackground = true
                    this.$store.dispatch("handleInternalError", error)
                })
        },
        downloadClicked() {
            const linkElement = document.getElementById("solution_link_element")
            linkElement.click()
            this.$store.dispatch("addNotification", {
                type: "SUCCESS",
                text: "Schedule downloaded"
            })
            linkElement.remove()
        },
        isUploadFieldsValid() {
            const isDatasetCodeValid = this.isTextFieldValid("upload_dataset_code", this.dataset_code_text)
            const isDescriptionValid = this.isObjectFieldValid("device_description_field", this.device_description_file)
            const isComfortValid = this.isObjectFieldValid("device_comfort_field", this.comfort_file)
            const isUsageValid = this.isObjectFieldValid("device_usage_field", this.initial_usage_file)

            if (!isDatasetCodeValid || !isDescriptionValid || !isComfortValid || !isUsageValid) {
                return false
            }

            return true
        },
        isTextFieldValid(fieldId, field) {
            const datasetCodeField = document.getElementById(fieldId)
            if (field == null || field === "") {
                datasetCodeField.style.backgroundColor = "#f1cdc2"
                return false
            }
            datasetCodeField.style.backgroundColor = "#ffffff"
            return true
        },
        isObjectFieldValid(fieldId, field) {
            const descriptionField = document.getElementById(fieldId)
            if (field == null) {
                descriptionField.style.backgroundColor = "#f1cdc2"
                return false
            }
            descriptionField.style.backgroundColor = "#ffffff"
            return true
        },
        deviceDescriptionFileUploadAction(file) {
            this.device_description_file = file
        },
        comfortDefinitionFileUploadAction(file) {
            this.comfort_file = file
        },
        usageDefinitionFileUploadAction(file) {
            this.initial_usage_file = file
        },
        deviceTargetCurveUploadAction(file) {
            this.target_curve_file = file
        },
        deviceConfigurationUploadAction(file) {
            this.configuration_file = file
        },
        resetResultBlock() {
            this.showTable = false
            this.showEmptyBackground = true
            this.showTextResult = false
            this.tables = []
            this.textResult = ""
            this.charts = []
            this.showChart = false
            this.showDownload = false
            this.showScheduleTable = false
            this.tables_schedule = []
            this.showLoading = false
        },
        startLoading() {
            this.showEmptyBackground = false
            this.showLoading = true
        },
        endLoading() {
           this.showLoading = false
        },
        scrollToResult() {
            this.$refs.resultSection.scrollIntoView({behavior: 'smooth', block: 'start'})
        }
    },
    beforeCreate() {
        const allDatasetCodesURL = "http://" + process.env.VUE_APP_SERVER_IP + ":" + process.env.VUE_APP_SERVER_PORT + "/scheduler/datasets"
        axios.get(allDatasetCodesURL)
            .then(result => {
                this.existingDatasetCodes = result.data
                if (result.data.length > 0) {
                    this.selected_dataset_code = result.data[0]
                }
            })
            .catch(error => {
                this.$store.dispatch("handleInternalError", error)
            })

        const availableOperationCodesURL = "http://" + process.env.VUE_APP_SERVER_IP + ":" + process.env.VUE_APP_SERVER_PORT + "/scheduler/operationCodes"
        axios.get(availableOperationCodesURL)
            .then(result => {
                this.availableOperationCodes = result.data
                if (result.data.length > 0) {
                    this.selected_operation_code = result.data[0]
                }
            })
            .catch(error => {
                this.$store.dispatch("handleInternalError", error)
            })
    }
}