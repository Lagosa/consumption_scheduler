<script src="./UploadPage.js"></script>

<template>
  <div class="relative w-full h-screen">
    <div class="absolute inset-0 z-10">
      <img class="object-cover w-full h-full"
           src="../../assets/background.jpg"
      />
    </div>
    <div class="absolute inset-0 bg-gray-50 opacity-95 z-20"></div>
    <div class="absolute inset-0 z-30 overflow-auto ">
      <div class="flex flex-grow h-2/3 w-11/12 mt-20 m-auto">
        <div class="px-5 h-full w-full m-auto">
          <HeaderBand :titles="['Upload', 'Operations']"/>
          <div class="flex flex-grow bg-white bg-opacity-60 h-5/6 w-full shadow-md ">
            <div class="h-full w-1/2 flex align-middle items-center">
              <div class="flex flex-grow border-r-2 h-5/6 justify-center">
                <div class="w-3/4">
                  <EditRow id="upload_dataset_code" :input-type="'TEXT'" :label="'Dataset code'"
                           v-model:value="this.dataset_code_text"/>
                  <EditRow id="device_description_field" :input-type="'UPLOAD'" :label="'Device description'"
                           @fileUploaded="deviceDescriptionFileUploadAction"/>
                  <EditRow id="device_comfort_field" :input-type="'UPLOAD'" :label="'Comfort definition'"
                           @fileUploaded="comfortDefinitionFileUploadAction"/>
                  <EditRow id="device_usage_field" :input-type="'UPLOAD'" :label="'Initial usage'"
                           @fileUploaded="usageDefinitionFileUploadAction"/>
                  <div class="flex flex-grow justify-center mt-10">
                    <UploadButton @clicked="doUpload"/>
                  </div>
                </div>
              </div>
            </div>
            <div class="h-full w-1/2 flex align-middle items-center">
              <div class="flex flex-grow h-5/6 justify-center">
                <div class="w-3/4">
                  <EditRow :input-type="'SEL'" :label="'Dataset code'" :select-options="this.existingDatasetCodes"
                           v-model:value="this.selected_dataset_code"/>
                  <EditRow :input-type="'SEL'" :label="'Operation code'" :select-options="this.availableOperationCodes"
                           v-model:value="this.selected_operation_code"/>
                  <EditRow :input-type="'UPLOAD'" :label="'Target curve'" @fileUploaded="deviceTargetCurveUploadAction"/>
                  <EditRow id="configuration_field" :input-type="'UPLOAD'" :label="'Configuration'" @fileUploaded="deviceConfigurationUploadAction"/>
                  <div class="flex flex-grow justify-center mt-10">
                    <OperationsButton @clicked="doScheduling"/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div ref="resultSection" class="rounded-lg w-10/12 shadow-md m-auto">
        <HeaderBand :titles="['Result']"/>
        <div class="bg-white bg-opacity-80 w-full mb-10">
          <div class="relative float m-auto" v-if="this.showEmptyBackground">
            <img src="@/assets/no-task.png" class="h-80 m-auto p-10 z-30" alt="Pictogram showing that not task is running">
            <div class="absolute inset-y-0 bg-white opacity-70 z-40 h-full w-full"></div>
          </div>
          <div v-if="this.showLoading">
            <img src="@/assets/loading.gif" class="h-80 m-auto p-10 z-30" alt="Pictogram showing that not task is running">
          </div>
          <div class="relative float m-auto px-5 py-10" v-if="!this.showEmptyBackground">
            <div v-if="this.showTextResult">
              {{ this.textResult }}
            </div>
            <div v-if="this.showTable">
              <TableComponent v-for="(table, index) in this.tables" v-bind:key="index" :title="table.title" :include_title="true" :data="table.data"
                              :header="table.header"/>
            </div>
            <div v-if="this.showChart">
              <ChartContainer v-for="(chart, index) in this.charts" v-bind:key="index" :chart="chart" />
            </div>
            <div v-if="this.showScheduleTable">
              <div class="text-lg font-semibold text-center mb-5">
                Schedule:
              </div>
              <div v-if="this.showDownload">
                <DownloadButton @clicked="this.downloadClicked"/>
              </div>
<!--              <TableComponent v-for="(table, index) in this.tables_schedule" v-bind:key="index" :title="table.title" :include_title="false" :data="table.data"-->
<!--                              :header="table.header"/>-->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


