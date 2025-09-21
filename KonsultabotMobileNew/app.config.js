export default {
  expo: {
    name: "Konsultabot",
    slug: "konsultabot-mobile",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    userInterfaceStyle: "light",
    splash: {
      image: "./assets/adaptive-icon.png",
      resizeMode: "contain",
      backgroundColor: "#ffffff"
    },
    assetBundlePatterns: [
      "**/*"
    ],
    ios: {
      supportsTablet: true
    },
    android: {
      adaptiveIcon: {
        foregroundImage: "./assets/adaptive-icon.png",
        backgroundColor: "#FFFFFF"
      }
    },
    web: {
      favicon: "./assets/favicon.png"
    },
    extra: {
      apiUrl: "http://localhost:8000/api"
    },
    plugins: [
      "expo-secure-store",
      [
        "expo-av",
        {
          microphonePermission: "Allow Konsultabot to access your microphone for voice input."
        }
      ]
    ]
  }
};
