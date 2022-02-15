// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import Amplify from 'aws-amplify';
import router from './router'
import { AWSIoTProvider } from '@aws-amplify/pubsub';
import aws_exports from './aws-exports';
import {
  applyPolyfills,
  defineCustomElements,
} from '@aws-amplify/ui-components/loader';

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

Amplify.addPluggable(new AWSIoTProvider({
  aws_pubsub_region: '[...Region of your AWS IoT Core...]',
      aws_pubsub_endpoint: 'wss://[...Device data endpoint found in IoT Core > Settings...]/mqtt',
}));

Amplify.configure(aws_exports);
applyPolyfills().then(() => {
  defineCustomElements(window);
});

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')