class Rise < ApplicationRecord
  has_one_attached :image

  validates :win_title, presence: true
  validates :dora, presence: true
  validates :dora_ura, presence: true
  validates :round_wind, presence: true
  validates :image, presence: true

  # ここから
  include Rails.application.routes.url_helpers
  # ここまでを追加してください。

  #　ここから
  def image_url
    image.attached? ? url_for(image) : nil
  end

  #　ここまで追加してください
end
