<!--
  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
  SPDX-License-Identifier: MIT-0
-->

<template>
   <div>
        <b-container>
          <h2>Add New Vehicle</h2>
        </b-container>
        <b-container>
          <b-row>
            <b-col sm="3">
              <label :for="vin_number">Vin Number</label>
            </b-col>
            <b-col sm="9">
              <b-form-input 
                id="vin_number" 
                type="text" 
                v-model="vin_number"
                :state="vinState"
                aria-describedby="input-live-help input-live-feedback"
              ></b-form-input>
              <b-form-invalid-feedback id="input-live-feedback">
                VIN must be 17 digits.
              </b-form-invalid-feedback>
              <b-form-text id="input-live-help">Enter the vehicles VIN.</b-form-text>
            </b-col>
          </b-row>
           <b-row style="padding-top: 20px; padding-bottom: 20px">
             <b-col offset="3" sm="3">
                <b-button @click="addVehicle" width="100%">Confirm</b-button>
            </b-col>
            <b-col sm="3">
              <b-button @click="goToHome" width="100%">Cancel</b-button>
            </b-col>
            <b-col sm="3">
            </b-col>
          </b-row>
        </b-container>
   </div>
</template>

<script>
import { API } from 'aws-amplify';
export default {
  name: 'add',
  computed: {
      vinState() {
        return this.vin_number.length == 17 ? true : false
      }
    },
  data() {
    return {
      vin_number: ''
    }
  },
  methods: {
    goToHome() {
        this.$router.push({name: 'home'})
    },
    async addVehicle() {
      const apiName = 'cvdatahandling';
      const path = '/vehicle/add'; 
      const myInit = { 
          headers: {},
          response: true, 
          queryStringParameters: { 
              "vin": this.vin_number,
          }
      }
      if(this.vin_number.length == 17) {
        API
        .get(apiName, path, myInit)
        .then(this.$router.push({name: 'home'}))
        .catch(error => {
          console.log("error")
          console.log(error)
          console.log(error.response)
        })
      }
    }
  }
}
</script>