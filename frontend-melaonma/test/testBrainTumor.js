import { S3Client, ListObjectsV2Command } from '@aws-sdk/client-s3';
import 'dotenv/config';

// get all objects from the bucket
// test the API and get the percentage correct

const ACCESS_KEY_ID = process.env.ACCESS_KEY_ID;
const SECRET_ACCESS_KEY = process.env.SECRET_ACCESS_KEY;

const s3Client = new S3Client({
  endpoint: 'https://f24d1f62bfe4b558707bd595d5b952da.r2.cloudflarestorage.com',
  region: 'auto',
  credentials: {
    accessKeyId: ACCESS_KEY_ID,
    secretAccessKey: SECRET_ACCESS_KEY,
  },
});

const getBucketKeys = async () => {
  const params = {
    Bucket: 'detect-brain-tumor',
  };

  const keys = [];

  try {
    let isTruncated = true;

    while (isTruncated) {
      const command = new ListObjectsV2Command(params);
      const response = await s3Client.send(command);

      response.Contents?.forEach((item) => {
        if (item.Key) {
          keys.push(item.Key);
        }
      });

      isTruncated = response.IsTruncated ?? false;

      if (response.NextContinuationToken) {
        params.ContinuationToken = response.NextContinuationToken;
      }
    }

    return keys;
  } catch (error) {
    console.error('Error:', error);
  }
};

const getMatchingKeys = (keys, folder) => {
  const matchedKeys = keys.filter((key) => key.startsWith(folder));
  return matchedKeys;
};

const testAccuracy = async (keys, targetClass) => {
  const chunkSize = 10;

  const allResults = [];

  for (let i = 0; i < keys.length; i += chunkSize) {
    const chunk = keys.slice(i, i + chunkSize);

    const targetURLs = chunk.map(
      (el) => `https://www.brain-tumor-static.nbaron.com/${el}`
    );

    const promises = targetURLs.map((url) => {
      return fetch(`http://0.0.0.0:8000/brain-tumor/predict-url`, {
        method: 'POST',
        body: JSON.stringify({ url }),
        headers: {
          'Content-Type': 'application/json',
        },
      }).then((res) => res.json());
    });

    const results = await Promise.all(promises);

    allResults.push(...results);
  }

  const correctResults = allResults.filter(({ classification }) => {
    return classification === targetClass;
  });

  const targetAccuracy = (correctResults.length / allResults.length) * 100;

  return targetAccuracy;
};

const testModel = async () => {
  const keys = await getBucketKeys();

  if (keys == undefined) {
    console.log('Failed to get object keys');
    return;
  }

  const gilomaKeys = getMatchingKeys(keys, 'giloma/');
  const meningiomaKeys = getMatchingKeys(keys, 'meningioma/');
  const noTumorKeys = getMatchingKeys(keys, 'notumor/');
  const pituitaryKeys = getMatchingKeys(keys, 'pituitary/');

  const gliomaAccuracy = await testAccuracy(gilomaKeys, 0);
  const meningiomaAccuracy = await testAccuracy(meningiomaKeys, 1);
  const noTumorAccuracy = await testAccuracy(noTumorKeys, 2);
  const pituitaryAccuracy = await testAccuracy(pituitaryKeys, 3);

  const combinedAccuracy =
    (gliomaAccuracy +
      meningiomaAccuracy +
      noTumorAccuracy +
      pituitaryAccuracy) /
    4;

  return combinedAccuracy;
};

testModel().then((acc) => {
  console.log(`Accuracy: ${acc}`);
});
