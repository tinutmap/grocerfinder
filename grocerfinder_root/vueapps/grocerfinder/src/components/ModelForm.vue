/* eslint-disable vue/no-mutating-props */
<template >
  <form class="form-group">
    <p
      v-for="i in okMessages"
      :key="i.key"
      :value="i.value"
      class="alert alert-success"
    >
      {{ i }}
    </p>
    <ul v-if="nonFieldErrors.length > 0" class="alert alert-warning">
      <li v-for="i in nonFieldErrors" :key="i.key" :value="i.value">
        {{ i }}
      </li>
    </ul>
    <ul v-if="hiddenErrors.length > 0" class="alert alert-warning">
      <li v-for="i in hiddenErrors" :key="i.key" :value="i.value">
        {{ i }}
      </li>
    </ul>
    <div v-for="key in Object.keys(formData)" :key="key">
      <label :for="'field-' + key" class="control-label">{{
        camelCaseToSentenceCase(key)
      }}</label>
      <span :id="'field-errors-' + key" class="error-field text-danger">
        {{ fieldErrors[key] }}
      </span>
      <br />
      <input
        v-if="formElement[key] === 'input-text'"
        type="text"
        required
        :id="'field-' + key"
        v-model.trim="formData[key]"
        class="form-control"
        v-bind:class="{ 'is-invalid': fieldErrors[key] }"
      />
      <input
        v-else-if="formElement[key] === 'input-number'"
        type="number"
        required
        :id="'field-' + key"
        v-model.number="formData[key]"
        class="form-control"
        v-bind:class="{ 'is-invalid': fieldErrors[key] }"
      />
      <select
        v-else-if="formElement[key] === 'select-option'"
        v-model="formData[key].id"
        :id="'field-' + key"
        class="form-control"
        required
      >
        <option disabled v-if="isNew" value="">--Select {{ key }}--</option>
        <option
          v-for="i in selectOptionData[key]"
          v-bind:key="i.id"
          v-bind:value="i.id"
          v-bind:selected="i.id === formData[key].id"
          v-bind:class="{ 'is-invalid': fieldErrors[key] }"
        >
          {{ i.name }}
        </option>
      </select>
    </div>
    <input
      type="button"
      v-if="isNew"
      value="Create"
      @click="$emit('create')"
      class="btn btn-primary"
    />
    <input
      type="button"
      v-else
      value="Update"
      @click="$emit('update')"
      class="btn btn-primary"
    />
  </form>
</template>
<script>
import { camelCaseToSentenceCase } from './Base.js'
export default {
  name: 'ModelForm',
  data: function () {
    return {}
  },
  props: {
    modelName: {
      type: String,
      required: true
    },
    formData: {
      type: Object
    },
    isNew: {
      type: Boolean,
      required: true,
      default: true
    },
    selectOptionData: {
      type: Object
    },
    formElement: {
      type: Object,
      required: true
    },
    nonFieldErrors: {
      type: Array
    },
    fieldErrors: {
      type: Object
    },
    hiddenErrors: {
      type: Array
    },
    okMessages: {
      type: Array
    }
  },
  methods: {
    camelCaseToSentenceCase
  }
}
</script>
