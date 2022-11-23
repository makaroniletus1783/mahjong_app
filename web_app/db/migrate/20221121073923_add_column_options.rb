class AddColumnOptions < ActiveRecord::Migration[7.0]
  def up
    add_column :rises, :win_title, :string
    add_column :rises, :dora, :string
    add_column :rises, :dora_ura, :string
    add_column :rises, :player_wind, :string
    add_column :rises, :round_wind, :string
    add_column :rises, :is_richi, :boolean, default: false, null: false
    add_column :rises, :is_tumo, :boolean, default: false, null: false
    add_column :rises, :is_rinshan, :boolean, default: false, null: false
    add_column :rises, :is_ippatu, :boolean, default: false, null: false
    add_column :rises, :melds, :boolean, default: false, null: false
  end
end
