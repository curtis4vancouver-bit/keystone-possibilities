import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.keystone.commandcenter',
  appName: 'Keystone Possibilities',
  webDir: 'out',
  server: {
    iosScheme: 'https',
    androidScheme: 'https',
    cleartext: false
  }
};

export default config;
