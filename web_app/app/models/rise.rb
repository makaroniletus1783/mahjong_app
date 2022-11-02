class Rise < ApplicationRecord

  # ここから
  include Rails.application.routes.url_helpers
  # ここまでを追加してください。

  has_one_attached :image

  #　ここから
  def image_url
    image.attached? ? url_for(image) : nil
  end

  #　ここまで追加してください
end
