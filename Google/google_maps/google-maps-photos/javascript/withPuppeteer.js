const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const placeUrl =
  "https://www.google.com/maps/place/Starbucks/data=!4m7!3m6!1s0x549069a98254bd17:0xb2f64f75b3edf4c3!8m2!3d47.5319688!4d-122.1942498!16s%2Fg%2F1tdfmzpb!19sChIJF71UgqlpkFQRw_Tts3VP9rI?authuser=0&hl=en&rclk=1";

async function scrollPage(page) {
  let iterationsLength = 0;
  while (true) {
    let photosLength = await page.evaluate(() => {
      return document.querySelectorAll(".U39Pmb").length;
    });
    for (; iterationsLength < photosLength; iterationsLength++) {
      await page.waitForTimeout(200)
      await page.evaluate((iterationsLength) => {
        document.querySelectorAll(".U39Pmb")[iterationsLength].scrollIntoView()
      }, iterationsLength);
    }
    await page.waitForTimeout(5000)
    let newPhotosLength = await page.evaluate(() => {
      return document.querySelectorAll(".U39Pmb").length;
    });
    if (newPhotosLength === photosLength) break
  }
}

async function getPhotosLinks(page) {
  const photos = await page.evaluate(() => {
    return Array.from(document.querySelectorAll(".U39Pmb")).map((el) => {
      return {
        thumbnail: getComputedStyle(el).backgroundImage.slice(5, -2),
      };
    });
  });
  const scripts = await page.evaluate(() => {
    return Array.from(document.querySelectorAll("script")).map(el => el.outerHTML).join()
  })
  return {photos, scripts};
}

async function getLocalPlacePhotos() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  await page.setDefaultNavigationTimeout(60000);
  await page.goto(placeUrl);
  await page.waitForNavigation();

  await page.click(".Dx2nRe");
  await page.waitForTimeout(2000);
  await page.waitForSelector(".U39Pmb");

  await scrollPage(page);

  const {photos, scripts} = await getPhotosLinks(page);

  await browser.close();

  const validPhotos = photos.filter((el) => el.thumbnail.includes('https://lh5.googleusercontent.com/p'))

  const photoSizePattern = /"https:\/\/lh5\.googleusercontent\.com\/p\/(?<id>[^\\]+).+?\[(?<resolution>\d{2,},\d{2,})/gm; // https://regex101.com/r/zgxNOb/2
  const fullSizeData = [...scripts.matchAll(photoSizePattern)].map(({ groups }) => ({id: groups.id, resolution: groups.resolution}));

  validPhotos.forEach(el => {
    const idPattern = /https:\/\/lh5\.googleusercontent\.com\/p\/(?<id>[^\=]+)/gm;  // https://regex101.com/r/XxS3QC/1
    const id = [...el.thumbnail.matchAll(idPattern)].map(({ groups }) => groups.id)[0];
    const resolution = fullSizeData.find((dataEl) => dataEl.id === id)?.resolution.split(',')
    if (resolution) el.image = `https://lh5.googleusercontent.com/p/${id}=w${resolution[1]}-h${resolution[0]}-k-no`
  })

  return validPhotos;
}

module.exports = { getLocalPlacePhotos };
