# EPM UIF - Serverless API

***This repository aims to provide infrastructure for the API in development under [EPMKEY-21910](https://jsw.ibm.com/browse/EPMKEY-21910) epic.***

The amount of stuck pods became an increasing pain for us: whenever they happened, they would demand support requests followed by analysis that often resulted in simple and manual actions. Based on that, there arose a need to automate this process, in other words, to make us able to identify a stuck pod and take the appropriate action in a fully automatic way, transparent for both developer and user.

Well, but what is the best way to identify a stuck pod? The answer is simple: based on historical data, we can tell if something is taking longer than it should to run. That’s when the perfect opportunity arose to implement, for the first time, a **Serverless computing module**.
