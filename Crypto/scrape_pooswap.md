https://gist.github.com/dimitryzub/b1edd9322df8ad82d2f1d075fe209fd8

- <a href="#what_will_be_scraped">What will be scraped</a>
- <a href="#prerequisites">Prerequisites</a>
- <a href="#process">Process</a>
- <a href="#full_code">Full Code</a>
- <a href="#explanation">Explanation</a>
- <a href="#links">Links</a>
- <a href="#outro">Outro</a>

___

<h2 id="what_will_be_scraped">What will be scraped</h2>

![image](https://user-images.githubusercontent.com/78694043/155510155-acddea16-a29c-4588-8e8e-68435bb351da.png)

___


<h2 id="full_code">Full Code</h2>

```python
python code..
```

<h2 id="explanation">Explanation</h2>


We want to reverse engineer URL `data` parameter:

```lang-none
# full url 
https://poocoin.app/api2/candles-bsc?data=[YmLNHK6TU[Kblm4UXqKeF2FTYSSW2KsZ32XfnO6TU[KblJ1UVeONWKGSYebblF{U2S[fWqIVYeObmVzXYqCN1:VTUCQSGmOWHiWUWSCOl6VWU[OSFG2UVSCe2eqTYOKcYixZmetNFmrc4qOblG{TX25e2GYVnukcW[7Z4mKOlmrRkSTS2FyXXuHb1:IXUS[bl1zUVeSN16uVYiOb2qsVWSKfl2GXUSSb1[IUlSLcWqVRYeOblqFVnmKd1mucIWlS2[6[H2Hd1mrc3mOWG[1TXm4bWmuSoqbWYi4TXqwbV2J[{GQSWl1Uoq[OF6V[HiOSFqGUnqkNl2sWYeOWFG5XX2KNWG7VUKSWHirUWWXSV6FVlW[flVzTX5xQR%3E%3E

# data parameter
[YmLNHK6TU[Kblm4UXqKeF2FTYSSW2KsZ32XfnO6TU[KblJ1UVeONWKGSYebblF{U2S[fWqIVYeObmVzXYqCN1:VTUCQSGmOWHiWUWSCOl6VWU[OSFG2UVSCe2eqTYOKcYixZmetNFmrc4qOblG{TX25e2GYVnukcW[7Z4mKOlmrRkSTS2FyXXuHb1:IXUS[bl1zUVeSN16uVYiOb2qsVWSKfl2GXUSSb1[IUlSLcWqVRYeOblqFVnmKd1mucIWlS2[6[H2Hd1mrc3mOWG[1TXm4bWmuSoqbWYi4TXqwbV2J[{GQSWl1Uoq[OF6V[HiOSFqGUnqkNl2sWYeOWFG5XX2KNWG7VUKSWHirUWWXSV6FVlW[flVzTX5xQR%3E%3E
```

- data parameter contains token id, time interval, date, and limit argument which I believe is for candles amount to display.

Open dev tools, find relevant XHR request and go to JS source: 

![image](https://user-images.githubusercontent.com/78694043/155734199-a9cd96a4-4399-445c-b289-271b7a78534a.png)

Format JavaScript code:

![image](https://user-images.githubusercontent.com/78694043/155734872-d013c96a-dc74-48a5-b3b3-5fca9ae720bf.png)

Go up in the stack trace to see the formation of `data` URL argument:

![image](https://user-images.githubusercontent.com/282605/154670571-ac27d02c-81a2-4aa8-9107-808fa3b88a4e.png)

Evaluate `F`, `W`, `B` `I` variables to understand what's happening:

![image](https://user-images.githubusercontent.com/282605/154671155-250845f1-db4b-4c82-bc5a-ecf3043732c8.png)

`B = w(476)`:

![image](https://user-images.githubusercontent.com/78694043/155934403-325148f2-4373-4fa3-84cb-104256bb5b67.png)

`w()` returns function name:

![image](https://user-images.githubusercontent.com/78694043/155935122-5d8f907a-6142-4873-b7e9-2bb9a7794d65.png)


```js
var n = ["map", "70209pSjRdP", "13mXPpTk", "32970804XTFOSy", "33EDoYDa", "16914prTfjD", "charCodeAt", "680Pigxyq", "5194335PIAMSW", "stringify", "430dfxvAD", "21ASPctV", "&l=1", "4868dULKHq", "955100otFPGh", "substring", "QWRkcmVzcyI6IjB4MGM1REEwZjA3OTYyZGQwMjU2YzA3OTI0ODY", "4483450KFkYTE", "2303RvgaFj", "lpr", "host", "indexOf"];

function w(e, t) { return n[e - 467] }
```

`I` contains base64 encoded characters shifted by one charater code to the right:


```js
let obfuscatedFunctionName = w(476) // B = w(476),
obfuscatedFunctionName === n[9] && obfuscatedFunctionName === "QWRkcmVzcyI6IjB4MGM1REEwZjA3OTYyZGQwMjU2YzA3OTI0ODY" // => true

let base64CharactersOfParamsBase64 = btoa("" + prefixOfEncodedParams + obfuscatedFunctionName + suffixOfEncodedParams).split("") // I = (I = (I = (I = (I = btoa("" + W + B + S)).split(""))

let base64CharactersPlusOneOfParamsBase64 = base64CharactersOfParamsBase64.map(function(e) {
  let charCodePlusOne = e.charCodeAt() + 1 // e[w(488)](0) + 1; w(488) === "charCodeAt"
  return charCodePlusOne
}).map(function(e) { // w(482) === "map"
  return String.fromCharCode(e)
}).join("")
```

Which is effectively the same as:

```js
let base64CharactersPlusOneOfParamsBase64 = base64CharactersOfParamsBase64.map(e => String.fromCharCode(e.charCodeAt() + 1)).join("")
```

Example value and test

```js
base64CharactersPlusOneOfParamsBase64 === '[YmLNHK6TU[Kblm4UXqKeF2FTYSSW2KsZ32XfnO6TU[KblJ1UVeONWKGSYebblF{U2S[fWqIVYeObmVzXYqCN1:VTUCQSGmOWHiWUWSGOl6VRU[OSFG2UVSCe2eqTYOKcYixZmetNFmrc4qOblG{TX25e2GYVnukcW[7Z4mKOlmrRkSOWGKFUmSsNF2rTYmOWFFzUXqofmqIVUKTSFVyUmeKOWqFRYe[WHtxUUKKOV6FSUGOflFzUnmKd1mucIWlS2[6[H2Hd1mrc3mOWG[1TXm4bWmuSoqbWYi4TXqwbV2J[4mPSHyrXlSCNV6FXUWPNmlxUWeSN11xXYiSWHe5Xn2Ge2KrWYmPfnyuXUKPcF1zUlePflKrTX5xQR>>' // => true
base64CharactersPlusOneOfParamsBase64 === I // => true
```

Now compare it with string in request:


```
https://poocoin.app/api2/candles-bsc?data=[YmLNHK6TU[Kblm4UXqKeF2FTYSSW2KsZ32XfnO6TU[KblJ1UVeONWKGSYebblF{U2S[fWqIVYeObmVzXYqCN1:VTUCQSGmOWHiWUWSGOl6VRU[OSFG2UVSCe2eqTYOKcYixZmetNFmrc4qOblG{TX25e2GYVnukcW[7Z4mKOlmrRkSOWGKFUmSsNF2rTYmOWFFzUXqofmqIVUKTSFVyUmeKOWqFRYe[WHtxUUKKOV6FSUGOflFzUnmKd1mucIWlS2[6[H2Hd1mrc3mOWG[1TXm4bWmuSoqbWYi4TXqwbV2J[4mPSHyrXlSCNV6FXUWPNmlxUWeSN11xXYiSWHe5Xn2Ge2KrWYmPfnyuXUKPcF1zUlePflKrTX5xQR%3E%3E
```

![image](https://user-images.githubusercontent.com/282605/154679736-8a4bb4b1-3352-4e64-8f11-b35fff49b72d.png)

___

<h2 id="links">Links</h2>

- [Code in the online IDE]()
- [API]()

___

<h2 id="outro">Outro</h2>

If you have anything to share, any questions, suggestions, or something that isn't working correctly, feel free to drop a comment in the
comment section or reach out via Twitter at [@dimitryzub](https://twitter.com/DimitryZub), or [@serp_api](https://twitter.com/serp_api).

Yours, Dmitriy, and the rest of SerpApi Team.


___

<p style="text-align: center;">Join us on <a href="https://www.reddit.com/r/SerpApi/">Reddit</a> | <a href="https://twitter.com/serp_api">Twitter</a> | <a href="https://www.youtube.com/channel/UCUgIHlYBOD3yA3yDIRhg_mg">YouTube</a></p>

<p style="text-align: center;">Add a  <a href="https://forum.serpapi.com/feature-requests">Feature Request</a>💫 or a <a href="https://forum.serpapi.com/bugs">Bug</a>🐞</p>

