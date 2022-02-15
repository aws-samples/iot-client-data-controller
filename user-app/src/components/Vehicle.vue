<!--
  Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
  SPDX-License-Identifier: MIT-0
-->

<template>
   <div>
     <b-container>
        <b-row>
          <b-col>
            <h3>C220 - {{ vin_number }}</h3>
          </b-col>
        </b-row>

        <b-row>
          <b-col>
            <b-card no-body>
                <b-tabs card>
                    <b-tab title="Safety Features" active>
                        <b-card-text>
                            <b-row>
                                <b-form-checkbox
                                    id="ckbDTC"
                                    v-model="dtc_bool"
                                    >
                                      Check sensor data for anamolies to warn of potential issues
                                </b-form-checkbox>
                            </b-row>
                        </b-card-text>
                    </b-tab>
                    <b-tab title="Trip Data">
                        <b-card-text>
                            <b-row>
                            <b-form-checkbox
                                id="ckbTrip"
                                v-model="trip_bool"
                                >
                                Store my trip data
                            </b-form-checkbox>
                            </b-row>
                            <b-row>
                            <b-form-checkbox
                                id="chkTelemetry"
                                v-model="telemetry_bool"
                                >
                                Calculate Driver safety score
                            </b-form-checkbox>
                            </b-row>
                            <b-row>
                            <b-form-checkbox
                                id="ckbMarketing"
                                v-model="marketing_bool"
                                >
                                Send recommendations based on my location
                            </b-form-checkbox>
                            </b-row>
                        </b-card-text>
                    </b-tab>
                    <b-tab title="Publish and Earn" active>
                        <b-card-text>
                            <b-row>
                                <b-form-checkbox
                                    id="chkSell"
                                    v-model="sell_bool"
                                    >
                                      Publish on marketplace and earn money
                                </b-form-checkbox>
                            </b-row>
                        </b-card-text>
                    </b-tab>
                </b-tabs>
            </b-card>
            </b-col>
        </b-row>
     </b-container>

     <b-container>
       <b-row style="padding-top: 20px; padding-bottom: 20px">
             <b-col offset="3" sm="3">
                <b-button @click="updateConfig" width="100%">Save</b-button>
            </b-col>
            <b-col sm="3">
              <b-button @click="goToHome" width="100%">Finished</b-button>
            </b-col>
            <b-col sm="3">
            </b-col>
          </b-row>
      </b-container>
   </div>
</template>

<script>
import { PubSub } from 'aws-amplify';

export default {
  name: 'vehicle',
  data() {
    return {
      vin_number: "",
      model_name: "",
      trip_bool: false,
      dtc_bool: false,
      telemetry_bool: false,
      marketing_bool: false,
      sell_bool: false,
      latest: { }
    }
  },
  mounted: function() {
      let vin = this.$route.params.vin_number
      this.vin_number = vin
      let _vm = this
      let dataTopic = "$aws/things/" + vin + "/shadow/name/" + vin + "/get/accepted"
      PubSub.subscribe(dataTopic).subscribe({
          next: data => {
            var somedoc = data.value.state.desired
            _vm.latest = somedoc
            _vm.displayConfig()
          },
          error: error => console.error(error),
          close: () => console.log('Done'),
      })
      setTimeout(function () {
        _vm.getConfig()
      }, 2000)
  },
  methods: {
    goToHome() {
        this.$router.push({name: 'home'})
    },
    async getConfig() {
      var getDataTopic = "$aws/things/" + this.vin_number + "/shadow/name/" + this.vin_number + "/get"
      await PubSub.publish(getDataTopic, { subtopic: 'get_data' })
      .then(() => { console.log("data retrieval started")})
      .catch(err => { console.log(err)})
    },
    displayConfig: function() {
      var desired = this.latest
      var temp = false
      if((desired['trip_bool'] == null) || (desired['trip_bool'] == '') || (desired['trip_bool']['timestamp'] > 0)) {
        temp = false
      }else{
        temp = desired['trip_bool']
      }
      console.log(temp)
      this.trip_bool = temp

      if((desired['dtc_bool'] == null) || (desired['dtc_bool'] == '') || (desired['dtc_bool']['timestamp'] > 0)) {
        temp = false
      }else{
        temp = desired['dtc_bool']
      }
      console.log(temp)
      this.dtc_bool = temp

      if((desired['telemetry_bool'] == null) || (desired['telemetry_bool'] == '') || (desired['telemetry_bool']['timestamp'] > 0)) {
        temp = false
      }else{
        temp = desired['telemetry_bool']
      }
      console.log(temp)
      this.telemetry_bool = temp
    },
    async updateConfig() {
      var updateTopic = "$aws/things/" + this.vin_number + "/shadow/name/" + this.vin_number + "/update"
      var data = {
        "state": {
          "desired": {
            "trip_bool": this.trip_bool,
            "dtc_bool": this.dtc_bool,
            "telemetry_bool": this.telemetry_bool
          }
        }
      }
      console.log(data)
      await PubSub.publish(updateTopic, data)
      .then(() => { console.log("update started")})
      .catch(err => { console.log(err)})
    }
  }
}
</script>