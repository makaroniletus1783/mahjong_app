require "net/http"
require "uri"
require "json"

uri = URI.parse("http://127.0.0.1:8000/mahjong/predict")
request = Net::HTTP::Post.new(uri)
request.content_type = "application/json"
request["Accept"] = "application/json"
request.body = JSON.dump({
  "image_url" => "string",
})

req_options = {
  use_ssl: uri.scheme == "https",
}

response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
  http.request(request)
end

puts(response.body)
