module.exports = function(eleventyConfig) {
  // Copy assets folder to output
  eleventyConfig.addPassthroughCopy("src/assets");

  // Watch for changes in assets
  eleventyConfig.addWatchTarget("src/assets/");

  // Helper to get current year
  eleventyConfig.addShortcode("year", () => `${new Date().getFullYear()}`);

  // Filter to check if current page matches a nav item
  eleventyConfig.addFilter("isActiveNav", function(navUrl, pageUrl) {
    if (navUrl === "/" && pageUrl === "/") return true;
    if (navUrl !== "/" && pageUrl.startsWith(navUrl)) return true;
    return false;
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      layouts: "_includes/layouts",
      data: "_data"
    },
    templateFormats: ["njk", "html", "md"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};
