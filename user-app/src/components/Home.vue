<!--
  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
  SPDX-License-Identifier: MIT-0
-->

<template>
   <div>
        <b-container>
          <p>Welcome!</p>
        </b-container>
                <b-card-group>
                  <div v-for="(item, index) in vehicles" :key="index">
                  <b-card
                      title="C220 Coupe"
                      :sub-title=item.vin
                      class="xl-12"
                      @click="gotovehicle(item.vin)"
                  >             
                    <b-card-text>
                      <img src="../assets/car.png" />
                    </b-card-text>
                  </b-card>
                  <b-button @click="deletevehicle(item.vin)">
                    <b-icon icon="trash" font-scale="1"></b-icon>
                  </b-button>
                  </div>

                  <b-card
                      title="Add Vehicle"
                      class="xl-12"
                      @click="addvehicle()"
                  >
                    <b-card-text>
                      <b-icon icon="plus-circle" font-scale="7.5"></b-icon>
                    </b-card-text>
                  </b-card>
                </b-card-group>
   </div>
</template>

<script>
import { API } from 'aws-amplify';
export default {
  name: 'home',
  data() {
    return {
      vehicles: []
    }
  },
  mounted: async function() {
      const apiName = 'cvdatahandling';
      const path = '/vehicles'; 
      const myInit = { // OPTIONAL
          headers: {},
          response: true, // OPTIONAL (return the entire Axios response object instead of only response.data)
      }
      API
        .get(apiName, path, myInit)
        .then(response => {
          var tempList = []
          console.log(response.data)
          response.data.forEach(vin => {
            var entry = { vin: vin }
            tempList.push(entry)
          })
          this.vehicles = tempList
        })
        .catch(error => {
          console.log("error")
          console.log(error)
          console.log(error.response)
        })
  },
  methods: {
    gotovehicle(vin) {
        this.$router.push({name: 'vehicle', params: {vin_number: vin}})
    },
    addvehicle() {
        this.$router.push({name: 'add'})
    },
    deletevehicle(vin_number) {
      console.log(vin_number)
      const apiName = 'cvdatahandling';
      const path = '/vehicle/delete'; 
      const myInit = { 
          headers: {},
          response: true, // OPTIONAL (return the entire Axios response object instead of only response.data)
          queryStringParameters: {  // OPTIONAL
              "vin": vin_number,
          }
      }
      API
        .get(apiName, path, myInit)
        .then(console.log("deleted"))
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>