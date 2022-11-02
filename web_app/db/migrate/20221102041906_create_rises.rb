class CreateRises < ActiveRecord::Migration[7.0]
  def change
    create_table :rises do |t|

      t.timestamps
    end
  end
end
