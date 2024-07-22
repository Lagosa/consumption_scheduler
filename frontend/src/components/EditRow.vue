<template>
  <div class="flex justify-center mt-5 ">
    <div class="w-11/12 flex border-b-2 text-lg justify-center border-b-main-color">
      <div class="mx-2 font-semibold w-1/2 space-x-5 text-right">
        {{ label }}:
      </div>
      <div class="mx-2 space-x-5 w-1/2">
        <input v-if="inputType === 'TEXT'" style="background: transparent" type="text" :value="value"
               @input="updateValue" class="w-11/12 px-2 focus:outline-none bg-white">
        <input v-if="inputType === 'NUMBER'" type="number" :value="value" @input="updateValue"
               class="w-11/12 px-2 focus:outline-none bg-white">
        <input v-if="inputType === 'PASS'" type="password" :value="value" @input="updateValue"
               class="w-11/12 px-2 focus:outline-none bg-white">
        <select v-if="inputType === 'SEL'" class="bg-white w-11/12" @focusout="updateValue">
          <option v-for="(opt, index) in selectOptions" v-bind:key="index" :selected="opt === value">
            {{ opt }}
          </option>
        </select>
        <div v-if="inputType === 'DATE'">
          <VueDatePicker v-model="dateValueChanges" :no-hours-overlay="true" :time-picker="false"/>
        </div>
        <div v-if="inputType === 'UPLOAD'">
          <div class="flex align-middle">
            <input id="file_upload" class="w-11/12" type="file" @change="fileUploadChanged">
<!--            <DeleteButton @deleteActioned="clearFileUpload" class="h-6 w-6"/>-->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import VueDatePicker from "@vuepic/vue-datepicker";

export default {
  name: 'EditRow',
  components: {VueDatePicker},
  props: {
    label: String,
    value: String,
    inputType: String,
    selectOptions: Array,
  },
  data() {
    return {
      date: new Date()
    }
  },
  methods: {
    updateValue($event) {
      this.$emit('update:value', $event.target.value)
    },
    setOptionValue() {
    },
    fileUploadChanged($event) {
      const file = $event.target.files || $event.dataTransfer.files
      if (!file.length) {
        return;
      }
      this.$emit('fileUploaded', file)
    },
    clearFileUpload() {
      var fileUpload = document.getElementById("file_upload")
      fileUpload.value = ''

    }
  },
  computed: {
    dateValueChanges: {
      get() {
        return this.date
      },
      set(value) {
        this.date = value;
        this.$emit('dateSelected', value)
      }
    }
  }
}
</script>